# Next.js + FastAPI モノレポ（Docker対応）

## 概要
- Web: Next.js 14 (App Router)
- API: FastAPI (Python 3.13)
- 認証: Python側でJWT発行、Next側でCookie保存（HttpOnly / SameSite=Lax）
- DB: デフォルトは SQLite（ローカル簡易動作）。本番は PostgreSQL + RLS を想定

## クイックスタート（Docker）
1. `.env` を準備
2. `docker compose up --build -d`
3. ブラウザで `http://localhost:3000` を開く
   - 初期ログイン: `admin@example.com` / `admin123`
4. 停止/削除: `docker compose down -v`（ローカルDBも削除されます）

## ローカル実行（手動）
- API
  ```powershell
  cd python-api
  python -m venv .venv; .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt -r requirements-dev.txt
  $env:SESSION_SECRET='devsupersecret'
  $env:CORS_ORIGINS='http://localhost:3000'
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
- Web
  ```powershell
  cd apps/web
  pnpm install
  $env:API_BASE_URL='http://localhost:8000'
  $env:SESSION_SECRET='devsupersecret'
  pnpm dev
  ```

## 構成
- `apps/web`: Next.js フロントエンド
- `python-api`: FastAPI バックエンド

## メモ（既知の事象）
- Next.js 14 を使用中のため、開発時に「Next.js (14.x) is outdated」表示が出ることがあります。実行を阻害しない警告です。依存更新はネットワーク許可後に実施してください。
- サーバーコンポーネントからの相対パス `fetch('/api/...')` により Node.js 22 で `Failed to parse URL` が出る場合があるため、内部API呼び出しは絶対URLに修正済みです（`apps/web/app/me/page.tsx` と `apps/web/app/admin/page.tsx`）。

