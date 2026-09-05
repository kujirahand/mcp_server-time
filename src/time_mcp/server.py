from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("time")


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


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
