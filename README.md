# new-service-20250913

このプロジェクトは Node.js のゲートウェイ(`node-api`)と、Python(FastAPI)のバックエンド(`python-api`)で構成される最小雛形です。

## 起動手順（Windows/PowerShell）

### 1) Python バックエンド

```powershell
cd "$env:USERPROFILE\Desktop\new-service-20250913\python-api"
py -3.13 -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

- ヘルスチェック: http://127.0.0.1:8000/health

### 2) Node.js ゲートウェイ

別ターミナルで:

```powershell
cd "$env:USERPROFILE\Desktop\new-service-20250913\node-api"
pnpm install
pnpm dev
```

- ヘルスチェック: http://127.0.0.1:3000/health
- Python へのプロキシ例: http://127.0.0.1:3000/api/py/hello?name=masan → `python-api` の `/hello`

## 設計メモ
- Node.js: 認証/認可、リクエスト集約、静的配信、BFF(Backend For Frontend) 役。
- Python: ドメインロジックや数値計算、機械学習処理などを担当。

### 長所
- ライブラリ適合性の最大化（Web は Node、数値/ML は Python）
- 責務分離で故障切り分けが容易

### 短所
- デプロイ/監視/ローカル起動の複雑さ増

## 次の一手
- OpenAPI から TypeScript 型生成（例: `openapi-typescript`）
- テスト（Jest/Vitest, Pytest）と CI の追加
- コンテナ化（docker-compose で 2 サービス起動）
