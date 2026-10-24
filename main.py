from fastapi import FastAPI
from pydantic import BaseModel
from v9 import NexusV9_DeltaSync

app = FastAPI(title="NEXUS ENGINE V9 - DeltaSync PRO")

# Engine Start
v9_engine = NexusV9_DeltaSync()

class DeltaRequest(BaseModel):
    client_id: str
    data: dict

@app.get("/")
def home():
    return {
        "project": "NEXUS V9 - DeltaSync PRO",
        "owner": "Abhishek Pal",
        "location": "Jamshedpur, Jharkhand, India",
        "status": "LIVE",
        "endpoint": "/v9/delta"
    }

@app.post("/v9/delta")
def v9_delta(req: DeltaRequest):
    delta = v9_engine.sync(req.client_id, req.data)

    is_zero = len(delta) == 0

    return {
        "owner": "Abhishek Pal",
        "client_id": req.client_id,
        "delta": delta,
        "is_zero_packet": is_zero,
        "dispatched_bytes": len(str(delta)),
        "stats": v9_engine.stats,
        "message": "0 bytes dispatched (100% saved)" if is_zero else f"Only {len(delta)} keys sent"
    }

@app.get("/v9/stats")
def v9_stats():
    return {
        "owner": "Abhishek Pal",
        "stats": v9_engine.stats
    }
