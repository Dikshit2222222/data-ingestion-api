# Data Ingestion API

## Overview

This project implements a simple, asynchronous Data Ingestion API using FastAPI. It allows clients to submit lists of IDs for ingestion with a specified priority, processes them in batches with strict rate limiting, and provides real-time status updates for each ingestion request.

---

## Features

- **RESTful Endpoints**:  
  - `POST /ingest`: Submit a list of IDs and a priority (`HIGH`, `MEDIUM`, `LOW`).
  - `GET /status/{ingestion_id}`: Retrieve the status of an ingestion request and its batches.

- **Batch Processing**:  
  - IDs are split into batches of up to 3.
  - Each batch is processed asynchronously.

- **Priority Queue**:  
  - Batches are processed in order of priority (`HIGH` > `MEDIUM` > `LOW`), then by request time.

- **Rate Limiting**:  
  - Only one batch is processed every 5 seconds, simulating an external API rate limit.

- **Status Tracking**:  
  - Each batch and ingestion request has a status: `yet_to_start`, `triggered`, or `completed`.

- **In-Memory Persistence**:  
  - All ingestion and batch statuses are stored in memory for fast access.

---

## Design Choices

- **FastAPI** was chosen for its speed, async support, and automatic documentation.
- **In-Memory Store**:  
  - The `IngestionStore` class manages all ingestions, batches, and the processing queue.
  - This keeps the implementation simple and suitable for demonstration or local use.
- **Async Processing**:  
  - Batches are processed in the background using `asyncio`, ensuring the API remains responsive.
- **Priority Queue**:  
  - Python's `heapq` is used to efficiently manage batch processing order.
- **Rate Limiting**:  
  - The processor waits 5 seconds between batches to simulate external API limits.
- **Status API**:  
  - The `/status/{ingestion_id}` endpoint provides real-time feedback on ingestion progress.

---

## How to Run

1. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Start the server:**
    ```sh
    uvicorn app.main:app --reload
    ```

3. **API Documentation:**  
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API docs.

---

## Example Usage

### Submit an Ingestion Request

```json
POST /ingest
{
  "ids": [1, 2, 3, 4, 5],
  "priority": "HIGH"
}
```

**Response:**
```json
{
  "ingestion_id": "abc123"
}
```

### Check Status

```http
GET /status/abc123
```

**Response:**
```json
{
  "ingestion_id": "abc123",
  "status": "triggered",
  "batches": [
    {"batch_id": "...", "ids": [1, 2, 3], "status": "completed"},
    {"batch_id": "...", "ids": [4, 5], "status": "triggered"}
  ]
}
```

---

## Testing

- Run all tests with:
    ```sh
    pytest
    ```

---

## Notes

- This implementation uses in-memory storage and is intended for demonstration or local development.
- For production use, consider replacing the in-memory store with a persistent database and using a robust task queue (like Celery or RQ).

---
