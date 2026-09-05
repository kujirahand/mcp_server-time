# time-mcp

ローカルの現在時刻と、世界各国のタイムゾーンの日時を返す MCP サーバーです。

## ツール

| ツール | 引数 | 戻り値 | 説明 |
| --- | --- | --- | --- |
| `get_local_time` | *(なし)* | 時刻オブジェクト | サーバーが動作しているマシンのローカル現在日時を返す |
| `get_time_in_timezone` | `timezone` (文字列, 必須) — IANA 名。例: `Asia/Tokyo` | 時刻オブジェクト | 指定タイムゾーンの現在日時を返す。不明な名前ならエラー |
| `list_timezones` | `query` (文字列, 任意, 既定値 `""`) — 大文字小文字を無視した部分一致。空なら全件 | `string[]` | 利用可能な IANA タイムゾーン名 (最大200件) |
| `get_time_from_ntp` | `server` (文字列, 任意) — 短縮名かホスト名; `timezone` (文字列, 任意) — IANA 名。省略時はローカル | 時刻オブジェクト + `ntp_server`, `local_clock_offset_seconds` | ローカル時計ではなく公開 NTP サーバーから現在時刻を取得する |

各ツールが返す時刻オブジェクト:

| フィールド | 型 | 例 |
| --- | --- | --- |
| `timezone` | 文字列 | `Asia/Tokyo` |
| `datetime` | 文字列 (ISO 8601) | `2026-09-05T14:10:32.637530+09:00` |
| `date` | 文字列 | `2026-09-05` |
| `time` | 文字列 | `14:10:32` |
| `weekday` | 文字列 | `Saturday` |
| `utc_offset` | 文字列 | `+0900` |
| `unix_timestamp` | 整数 | `1788585032` |

`get_time_from_ntp` はさらに2つのフィールドを返します。`ntp_server` (実際に使用したホスト) と
`local_clock_offset_seconds` (マシンの時計と NTP 時刻とのずれ。正の値ならローカル時計が遅れている)。

### NTP サーバー

`server` には次の短縮名、または任意の NTP ホスト名を指定できます。

| 短縮名 | ホスト | 運用元 |
| --- | --- | --- |
| `apple` | `time.apple.com` | Apple |
| `microsoft` / `windows` | `time.windows.com` | Microsoft |
| `nict` | `ntp.nict.jp` | 情報通信研究機構 (NICT) |
| `google` | `time.google.com` | Google |
| `cloudflare` | `time.cloudflare.com` | Cloudflare |
| `pool` | `pool.ntp.org` | NTP Pool Project |

`server` を省略した場合は `time.apple.com` を先に試し、失敗したら `time.windows.com` を使います。
UDP 123番ポートでの外部通信が必要です。タイムアウトは5秒です。

## インストール

```sh
pip install time-mcp
```

インストールせずに実行する場合:

```sh
uvx time-mcp
```

## 開発用セットアップ

```sh
uv sync
```

## 動作確認

```sh
uv run mcp dev src/time_mcp/server.py
```

## Claude Code への登録

```sh
claude mcp add time -- uvx time-mcp
```

`claude_desktop_config.json` に書く場合:

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

## Codex CLI への登録

```sh
codex mcp add time -- uvx time-mcp
```

`~/.codex/config.toml` に直接書く場合:

```toml
[mcp_servers.time]
command = "uvx"
args = ["time-mcp"]
```

登録できたか確認する:

```sh
codex mcp list
```

## ローカルのソースから実行する場合

上記の設定の `uvx time-mcp` の部分を、次のように置き換えます。

```sh
uv --directory /path/to/mcp_server-time run time-mcp
```

## ライセンス

MIT ライセンスです。詳細は [LICENSE](LICENSE) を参照してください。

## 公開手順

PyPI への公開手順は [docs/publish-ja.md](docs/publish-ja.md) を参照してください。
