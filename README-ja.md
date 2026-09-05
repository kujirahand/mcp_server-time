# time-mcp

ローカルの現在時刻と、世界各国のタイムゾーンの日時を返す MCP サーバーです。

## ツール

| ツール | 引数 | 戻り値 | 説明 |
| --- | --- | --- | --- |
| `get_local_time` | *(なし)* | 時刻オブジェクト | サーバーが動作しているマシンのローカル現在日時を返す |
| `get_time_in_timezone` | `timezone` (文字列, 必須) — IANA 名。例: `Asia/Tokyo` | 時刻オブジェクト | 指定タイムゾーンの現在日時を返す。不明な名前ならエラー |
| `list_timezones` | `query` (文字列, 任意, 既定値 `""`) — 大文字小文字を無視した部分一致。空なら全件 | `string[]` | 利用可能な IANA タイムゾーン名 (最大200件) |

`get_local_time` と `get_time_in_timezone` が返す時刻オブジェクト:

| フィールド | 型 | 例 |
| --- | --- | --- |
| `timezone` | 文字列 | `Asia/Tokyo` |
| `datetime` | 文字列 (ISO 8601) | `2026-09-05T14:10:32.637530+09:00` |
| `date` | 文字列 | `2026-09-05` |
| `time` | 文字列 | `14:10:32` |
| `weekday` | 文字列 | `Saturday` |
| `utc_offset` | 文字列 | `+0900` |
| `unix_timestamp` | 整数 | `1788585032` |

## セットアップ

```sh
uv sync
```

## 動作確認

```sh
uv run mcp dev src/time_mcp/server.py
```

## Claude Code への登録

```sh
claude mcp add time -- uv --directory /Users/kujirahand/repos/mcp_server-time run time-mcp
```

`claude_desktop_config.json` に書く場合:

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

## ライセンス

MIT ライセンスです。詳細は [LICENSE](LICENSE) を参照してください。
