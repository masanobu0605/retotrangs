from fastapi import FastAPI

app = FastAPI(title="python-api")

@app.get("/health")
def health():
    return {"ok": True, "service": "python-api"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name} from python-api!"}
