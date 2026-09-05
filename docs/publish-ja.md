# PyPI 公開手順

`time-mcp` を PyPI に公開するときの手順です。

## 0. 事前準備（初回のみ）

- [PyPI](https://pypi.org/) と [TestPyPI](https://test.pypi.org/) のアカウントを作成する
- 二要素認証 (2FA) を有効にする（PyPI では必須）
- API トークンを発行する
  - PyPI: Account settings → API tokens → Add API token
  - 初回はプロジェクトが存在しないため、スコープは "Entire account" で発行する。公開後にプロジェクト単位のトークンへ切り替えるとより安全
- トークンを `~/.pypirc` に保存する（パーミッションは `chmod 600 ~/.pypirc`）

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxx

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxx
```

> `~/.pypirc` を使わない場合は、`twine upload` 実行時に username に `__token__`、password にトークン文字列を入力します。トークンは Git 管理下に置かないこと。

## 1. 公開前チェック

```sh
# 作業ツリーがクリーンか確認
git status

# 動作確認（MCP Inspector が開く）
uv run mcp dev src/time_mcp/server.py
```

- `pyproject.toml` の `version` を上げる（例: `0.1.0` → `0.1.1`）
  - 同じバージョンは **一度公開すると再アップロードできない**。削除しても同名では再利用不可
  - バージョンを上げたらコミットしておく
- README の内容が最新か（ツール一覧・引数の表）を確認する

## 2. ビルド

```sh
rm -rf dist
uv build
```

`dist/` に以下の2つができます。

- `time_mcp-<version>-py3-none-any.whl`
- `time_mcp-<version>.tar.gz`

## 3. パッケージの検証

```sh
uvx twine check dist/*
```

両方が `PASSED` になることを確認します。README の記法エラーはここで検出されます。

## 4. TestPyPI で試す（推奨）

```sh
uvx twine upload -r testpypi dist/*
```

別環境でインストールして動作確認します。依存パッケージ (`mcp` など) は本番 PyPI から取得させます。

```sh
uvx --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    time-mcp
```

## 5. 本番 PyPI へ公開

```sh
uvx twine upload dist/*
```

## 6. 公開後の確認

```sh
# ページを確認
open https://pypi.org/project/time-mcp/

# 実際にインストールして起動できるか
uvx time-mcp
```

Git のタグも打っておきます。

```sh
git tag v0.1.0
git push origin v0.1.0
```

## 補足: GitHub Actions からの自動公開 (Trusted Publisher)

トークンを保存せずに公開する方法です。

1. PyPI のプロジェクトページ → Publishing → Add a new publisher で以下を登録
   - Owner: `kujirahand`
   - Repository: `mcp_server-time`
   - Workflow name: `publish.yml`
   - Environment name: `pypi`
2. `.github/workflows/publish.yml` を作成し、タグ push 時に `pypa/gh-action-pypi-publish` を実行する
   - ジョブに `permissions: id-token: write` が必要
3. `git push origin v0.1.0` のようにタグを push すると自動で公開される

初回公開前でも "pending publisher" として登録できます。

## トラブルシューティング

| 症状 | 原因と対処 |
| --- | --- |
| `403 Forbidden` | トークンが誤っている、またはスコープ外。トークンを再発行する |
| `400 File already exists` | 同じバージョンが公開済み。`version` を上げて再ビルドする |
| `twine check` が FAILED | README の記法エラー。`readme = "README.md"` の内容を修正する |
| インストールしたのに `time-mcp` が無い | `[project.scripts]` の設定漏れ。`pyproject.toml` を確認する |
