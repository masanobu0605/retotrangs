# new-service-20250913

Node.js のゲートウェイ (`node-api`) と、Python(FastAPI) のバックエンド (`python-api`) を並走させる最小構成です。Windows + PowerShell を前提にしています。

## 構成
- `python-api/`: FastAPI アプリ（`/health`, `/hello`）
- `node-api/`: Node BFF（`/health` と `/api/py/*` を Python にプロキシ）
- `docker-compose.yml`: 2 サービスを起動（Node → Python を内部名で参照）

## 使い方（Docker）
Docker を使う最短手順です。

```powershell
cd "$env:USERPROFILE\Desktop\new-service-20250913"
docker compose pull
docker compose up -d
```

起動確認:

- Python: http://127.0.0.1:8000/health → `{ "ok": true, "service": "python-api" }`
- Node:   http://127.0.0.1:3000/health → `{ "ok": true, "service": "node-api" }`
- 経由確認: http://127.0.0.1:3000/api/py/hello?name=masan → Python の `/hello` へプロキシ

補足:
- 初回は Python コンテナ内で `pip install -r requirements.txt` が走るため少し時間がかかります。
- コンテナ停止は `docker compose down`。ログは `docker compose logs -f`。

## ローカル実行（開発）
### 1) Python（FastAPI）
```powershell
cd "$env:USERPROFILE\Desktop\new-service-20250913\python-api"
py -3.13 -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2) Node（BFF）
```powershell
cd "$env:USERPROFILE\Desktop\new-service-20250913\node-api"
pnpm install
pnpm dev
```

- Node Health: http://127.0.0.1:3000/health
- Python 経由: http://127.0.0.1:3000/api/py/hello?name=masan

## テスト
最小の統合テスト（Node 側）と、FastAPI の API テスト（Python 側）を追加しています。

```powershell
cd "$env:USERPROFILE\Desktop\new-service-20250913\node-api"
pnpm test
```

Python 側のテスト（ローカル仮想環境）:

```powershell
cd "$env:USERPROFILE\Desktop\new-service-20250913\python-api"
py -3.13 -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

今後の拡張（任意）
- Python 直叩きのテストを `pytest` + `TestClient` で追加
- OpenAPI から TypeScript 型生成（`openapi-typescript`）
- docker-compose に `healthcheck` を追加（済）
