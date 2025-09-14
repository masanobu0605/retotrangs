# ログ駆動の自動修正（Auto Fix from Docker Logs）

Docker/アプリのログから既知の失敗パターンを検知し、修正プランを提示/適用するツールを同梱しています。

- スクリプト: `scripts/auto_fix_from_docker_log.py`
- 入力: 標準入力 または `--from-file <path>` のログテキスト
- 出力: 検知した問題と対応プラン。`--apply` を付けるとファイルを自動修正

## 使い方

プラン出力（適用はしない）

```bash
python scripts/auto_fix_from_docker_log.py --from-file docker.log
```

自動修正を適用

```bash
python scripts/auto_fix_from_docker_log.py --from-file docker.log --apply
```

## 実装済みの検知/修正

- Next.js: `Failed to parse URL from /api...`
  - サーバー側 fetch を絶対URLへ正規化（`apps/web/lib/url.ts` と主要ページ修正）
- FastAPI: `Email already registered`
  - `/auth/register` を冪等化（既存メールは 200 で `{id}` を返却）

> 注意: 既に修正済みのコードがある場合は「skipped」と表示します。全ての問題を自動修正できるわけではありません。新規パターンは `scripts/auto_fix_from_docker_log.py` へルールを追加してください。

