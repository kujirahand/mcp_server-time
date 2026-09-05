import socket
import struct
import time
from datetime import datetime, timezone as dt_timezone
from zoneinfo import ZoneInfo, available_timezones

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("time")

# Well-known public NTP servers, addressable by a short name.
NTP_SERVERS = {
    "apple": "time.apple.com",
    "microsoft": "time.windows.com",
    "windows": "time.windows.com",
    "nict": "ntp.nict.jp",
    "google": "time.google.com",
    "cloudflare": "time.cloudflare.com",
    "pool": "pool.ntp.org",
}

# Tried in order when no server is given.
DEFAULT_NTP_SERVERS = ("time.apple.com", "time.windows.com")

# Seconds between the NTP epoch (1900-01-01) and the Unix epoch (1970-01-01).
NTP_UNIX_EPOCH_DELTA = 2_208_988_800
NTP_TIMEOUT_SECONDS = 5.0


def _describe(dt: datetime) -> dict:
    return {
        "timezone": str(dt.tzinfo),
        "datetime": dt.isoformat(),
        "date": dt.strftime("%Y-%m-%d"),
        "time": dt.strftime("%H:%M:%S"),
        "weekday": dt.strftime("%A"),
        "utc_offset": dt.strftime("%z"),
        "unix_timestamp": int(dt.timestamp()),
    }


@mcp.tool()
def get_local_time() -> dict:
    """Return the current local date and time of the machine running this server."""
    return _describe(datetime.now().astimezone())


@mcp.tool()
def get_time_in_timezone(timezone: str) -> dict:
    """Return the current date and time in the given IANA timezone (e.g. Asia/Tokyo, America/New_York)."""
    try:
        tz = ZoneInfo(timezone)
    except Exception:
        raise ToolError(
            f"Unknown timezone: {timezone!r}. "
            "Use an IANA name such as Asia/Tokyo, Europe/London or America/New_York. "
            "Call list_timezones to search for valid names."
        )
    return _describe(datetime.now(tz))


@mcp.tool()
def list_timezones(query: str = "") -> list[str]:
    """Search available IANA timezone names. `query` is a case-insensitive substring match."""
    names = sorted(available_timezones())
    if query:
        q = query.lower()
        names = [n for n in names if q in n.lower()]
    return names[:200]


def _query_ntp(host: str) -> tuple[float, float]:
    """Send an SNTP request to `host` and return (unix_time, clock_offset_seconds)."""
    packet = b"\x1b" + 47 * b"\0"  # LI=0, VN=3, Mode=3 (client)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(NTP_TIMEOUT_SECONDS)
        t1 = time.time()
        sock.sendto(packet, (host, 123))
        data, _ = sock.recvfrom(48)
        t4 = time.time()

    if len(data) < 48:
        raise OSError(f"short NTP reply from {host}: {len(data)} bytes")

    # Bytes 32-39: server receive timestamp, 40-47: server transmit timestamp.
    recv_int, recv_frac, tx_int, tx_frac = struct.unpack("!4I", data[32:48])
    if tx_int == 0:
        raise OSError(f"invalid NTP reply from {host}")
    t2 = recv_int + recv_frac / 2**32 - NTP_UNIX_EPOCH_DELTA
    t3 = tx_int + tx_frac / 2**32 - NTP_UNIX_EPOCH_DELTA
    offset = ((t2 - t1) + (t3 - t4)) / 2
    return t3, offset


@mcp.tool()
def get_time_from_ntp(server: str = "", timezone: str = "") -> dict:
    """Get the current time from a public NTP server instead of the local clock.

    `server` accepts a short name (apple, microsoft, windows, nict, google,
    cloudflare, pool) or a hostname. When omitted, time.apple.com is tried
    first and time.windows.com is used as a fallback.
    `timezone` is an IANA name for the returned time; the local timezone is
    used when omitted.
    """
    if server:
        hosts = [NTP_SERVERS.get(server.lower().strip(), server.strip())]
    else:
        hosts = list(DEFAULT_NTP_SERVERS)

    if timezone:
        try:
            tz = ZoneInfo(timezone)
        except Exception:
            raise ToolError(
                f"Unknown timezone: {timezone!r}. "
                "Call list_timezones to search for valid names."
            )
    else:
        tz = None

    errors = []
    for host in hosts:
        try:
            unix_time, offset = _query_ntp(host)
        except Exception as exc:
            errors.append(f"{host}: {exc}")
            continue
        dt = datetime.fromtimestamp(unix_time, dt_timezone.utc)
        result = _describe(dt.astimezone(tz) if tz else dt.astimezone())
        result["ntp_server"] = host
        result["local_clock_offset_seconds"] = round(offset, 6)
        return result

    raise ToolError(
        "Could not reach any NTP server (" + "; ".join(errors) + "). "
        "Known short names: " + ", ".join(sorted(NTP_SERVERS)) + "."
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
