# time-mcp

An MCP server that returns the local current time and the current time in any IANA timezone.

> [日本語はこちら(README-ja.md)](https://github.com/kujirahand/mcp_server-time/blob/main/README-ja.md)

## Tools

| Tool | Arguments | Returns | Description |
| --- | --- | --- | --- |
| `get_local_time` | *(none)* | time object | Current date and time of the machine running the server |
| `get_time_in_timezone` | `timezone` (string, required) — IANA name, e.g. `Asia/Tokyo` | time object | Current date and time in the given timezone. Errors if the name is unknown |
| `list_timezones` | `query` (string, optional, default `""`) — case-insensitive substring; empty returns all | `string[]` | Available IANA timezone names, max 200 results |
| `get_time_from_ntp` | `server` (string, optional) — short name or hostname; `timezone` (string, optional) — IANA name, defaults to local | time object + `ntp_server`, `local_clock_offset_seconds` | Current time from a public NTP server instead of the local clock |

The time object returned by the tools above:

| Field | Type | Example |
| --- | --- | --- |
| `timezone` | string | `Asia/Tokyo` |
| `datetime` | string (ISO 8601) | `2026-09-05T14:10:32.637530+09:00` |
| `date` | string | `2026-09-05` |
| `time` | string | `14:10:32` |
| `weekday` | string | `Saturday` |
| `utc_offset` | string | `+0900` |
| `unix_timestamp` | integer | `1788585032` |

`get_time_from_ntp` adds two fields: `ntp_server` (the host actually used) and
`local_clock_offset_seconds` (how far the machine's clock is from the NTP time;
positive means the local clock is behind).

### NTP servers

`server` takes one of these short names, or any NTP hostname.

| Short name | Host | Operator |
| --- | --- | --- |
| `apple` | `time.apple.com` | Apple |
| `microsoft` / `windows` | `time.windows.com` | Microsoft |
| `nict` | `ntp.nict.jp` | NICT (Japan) |
| `google` | `time.google.com` | Google |
| `cloudflare` | `time.cloudflare.com` | Cloudflare |
| `pool` | `pool.ntp.org` | NTP Pool Project |

When `server` is omitted, `time.apple.com` is tried first and `time.windows.com`
is used as a fallback. Requires outbound UDP port 123; the timeout is 5 seconds.

## Install

```sh
pip install time-mcp
```

Or run it without installing:

```sh
uvx time-mcp
```

## Development setup

```sh
uv sync
```

## Try it

```sh
uv run mcp dev src/time_mcp/server.py
```

## Register with Claude Code

```sh
claude mcp add time -- uvx time-mcp
```

Or in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["time-mcp"]
    }
  }
}
```

## Register with Codex CLI

```sh
codex mcp add time -- uvx time-mcp
```

Or add it to `~/.codex/config.toml` by hand:

```toml
[mcp_servers.time]
command = "uvx"
args = ["time-mcp"]
```

Check that it is registered:

```sh
codex mcp list
```

## Running from a local checkout

Replace `uvx time-mcp` with the following in any of the configurations above:

```sh
uv --directory /path/to/mcp_server-time run time-mcp
```

## License

MIT License. See [LICENSE](LICENSE).
