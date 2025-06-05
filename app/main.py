from fastapi import FastAPI, HTTPException
from app.models import IngestionRequest
from app.store import ingestion_store

app = FastAPI()

@app.post("/ingest")
async def ingest(request: IngestionRequest):
    ingestion_id = ingestion_store.create_ingestion(request)
    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}")
async def status(ingestion_id: str):
    result = ingestion_store.get_status(ingestion_id)
    if not result:
        raise HTTPException(status_code=404, detail="Ingestion ID not found")
    return result