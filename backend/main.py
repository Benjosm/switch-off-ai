from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uvicorn
import random

app = FastAPI(title="Switch Off AI API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for shutdown request
class ShutdownRequest(BaseModel):
    confirmation: str
    emergency: bool = False
    reason: Optional[str] = None

# In-memory state
ai_status = "active"

@app.get("/")
def read_root():
    return {"message": "Switch Off AI Backend"}

@app.get("/status")
def get_status():
    """Return current AI system status with extended health details."""
    health = random.choice(["healthy", "degraded", "warning"])
    return {
        "status": ai_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "health": health,
        "version": "1.0",
        "service": "switch-off-ai"
    }

@app.post("/api/shutdown", status_code=status.HTTP_200_OK)
def shutdown_ai(request: ShutdownRequest):
    """
    Endpoint to initiate AI shutdown.
    Requires confirmation message to be 'CONFIRM'.
    Supports emergency shutdown mode.
    """
    if request.confirmation != "CONFIRM":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shutdown requires confirmation='CONFIRM'"
        )
    
    global ai_status
    if ai_status == "shutdown":
        return {"message": "AI is already off", "status": ai_status}
    
    # Simulate shutdown
    ai_status = "emergency_offline" if request.emergency else "shutdown"
    
    return {
        "message": "AI shutdown initiated",
        "status": ai_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "emergency": request.emergency,
        "reason": request.reason or "No reason provided"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
