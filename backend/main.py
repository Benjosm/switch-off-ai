from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Switch Off AI API", version="0.1.0")

@app.get("/")
def read_root():
    return {"message": "Switch Off AI backend is running"}

@app.get("/status")
def get_status():
    return {"status": "ok", "service": "switch-off-ai"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
