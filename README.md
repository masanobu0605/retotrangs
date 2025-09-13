# Next.js + FastAPI 会員登録ツール (Docker対応)

## 概要
- フロント: Next.js (App Router)
- API: FastAPI (Python)
- 認証: Python側でJWT発行、Nextのミドルウェアで検証
- DB: SQLite (ボリューム永続化)

## かんたん起動 (Docker)
1. `.env.example` を参考に `.env` を作成
2. `docker compose up --build`
3. ブラウザで `http://localhost:3000` を開く
   - 管理ログイン: `admin@example.com` / `admin123` (初回起動時に作成)

## ローカル起動 (Docker なし)
- API
  ```powershell
  cd apps/api
  python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1
  pip install -r requirements.txt
  $env:SESSION_SECRET='devsupersecret'
  $env:DB_PATH=(Resolve-Path ./data/app.db)
  $env:CORS_ORIGINS='http://localhost:3000'
  $env:ADMIN_EMAIL='admin@example.com'
  $env:ADMIN_PASSWORD='admin123'
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
- Web
  ```powershell
  cd apps/web
  pnpm install
  $env:API_BASE_URL='http://localhost:8000'
  $env:SESSION_SECRET='devsupersecret'
  pnpm dev
  ```

## 機能
- 会員登録 (氏名/メール/パスワード)
- ログイン (管理者/一般ユーザー)
- 管理画面: 登録ユーザー一覧
- ユーザー画面: 自分の会員情報

## ディレクトリ
- `apps/web`: Next.js フロント
- `apps/api`: FastAPI バックエンド

## 注意
- 本実装は学習用の最小構成です。実運用では以下の強化を推奨:
  - パスワードポリシー/ロックアウト
  - HTTPS + セキュア/HttpOnly/SameSite Cookie設定
  - ログ/監査/レート制限
  - マイグレーションツール導入 (Alembic)

