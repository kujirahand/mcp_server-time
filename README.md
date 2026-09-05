# time-mcp

An MCP server that returns the local current time and the current time in any IANA timezone.

> [日本語はこちら(README-ja.md)](https://github.com/kujirahand/mcp_server-time/blob/main/README-ja.md)

## Tools

| Tool | Arguments | Returns | Description |
| --- | --- | --- | --- |
| `get_local_time` | *(none)* | time object | Current date and time of the machine running the server |
| `get_time_in_timezone` | `timezone` (string, required) — IANA name, e.g. `Asia/Tokyo` | time object | Current date and time in the given timezone. Errors if the name is unknown |
| `list_timezones` | `query` (string, optional, default `""`) — case-insensitive substring; empty returns all | `string[]` | Available IANA timezone names, max 200 results |

The time object returned by `get_local_time` and `get_time_in_timezone`:

| Field | Type | Example |
| --- | --- | --- |
| `timezone` | string | `Asia/Tokyo` |
| `datetime` | string (ISO 8601) | `2026-09-05T14:10:32.637530+09:00` |
| `date` | string | `2026-09-05` |
| `time` | string | `14:10:32` |
| `weekday` | string | `Saturday` |
| `utc_offset` | string | `+0900` |
| `unix_timestamp` | integer | `1788585032` |

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
claude mcp add time -- uv --directory /Users/kujirahand/repos/mcp_server-time run time-mcp
```

Or in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "time": {
      "command": "uv",
      "args": ["--directory", "/Users/kujirahand/repos/mcp_server-time", "run", "time-mcp"]
    }
  }
}
```

## License

MIT License. See [LICENSE](LICENSE).
