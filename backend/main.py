from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import time

app = FastAPI(title="Switch Off AI API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for shutdown request
class ShutdownRequest(BaseModel):
    confirmation: str
    reason: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Switch Off AI backend is running"}

@app.get("/status")
def get_status():
    return {
        "status": "ok",
        "service": "switch-off-ai",
        "timestamp": int(time.time())
    }

@app.post("/api/shutdown")
def request_shutdown(request: ShutdownRequest):
    if request.confirmation != "CONFIRM":
        raise HTTPException(
            status_code=400,
            detail="Shutdown request requires confirmation='CONFIRM'"
        )
    
    # Simulate safe shutdown procedure
    return {
        "status": "shutdown_initiated",
        "reason": request.reason or "No reason provided",
        "timestamp": int(time.time())
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
