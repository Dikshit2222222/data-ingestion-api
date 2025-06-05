import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_and_status():
    # Submit MEDIUM priority request
    medium_res = client.post("/ingest", json={
        "ids": [1, 2, 3, 4, 5],
        "priority": "MEDIUM"
    })
    
    assert medium_res.status_code == 200
    ingestion_id = medium_res.json()["ingestion_id"]

    # Check status of the MEDIUM priority request
    status_res = client.get(f"/status/{ingestion_id}")
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "yet_to_start"

    # Submit HIGH priority request
    high_res = client.post("/ingest", json={
        "ids": [6, 7, 8],
        "priority": "HIGH"
    })
    
    assert high_res.status_code == 200
    high_ingestion_id = high_res.json()["ingestion_id"]

    # Check status of the HIGH priority request
    status_high_res = client.get(f"/status/{high_ingestion_id}")
    assert status_high_res.status_code == 200
    assert status_high_res.json()["status"] == "yet_to_start"

    # Wait for processing to complete (this may need adjustment based on actual processing time)
    import time
    time.sleep(6)  # Wait longer than the rate limit

    # Check the status again
    status_res = client.get(f"/status/{ingestion_id}")
    assert status_res.json()["batches"][0]["status"] == "triggered"

    status_high_res = client.get(f"/status/{high_ingestion_id}")
    assert status_high_res.json()["batches"][0]["status"] == "triggered"