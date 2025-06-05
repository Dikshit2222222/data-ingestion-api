from uuid import uuid4
import asyncio
import heapq
import time

BATCH_SIZE = 3
PRIORITY_MAP = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

class IngestionStore:
    def __init__(self):
        self.ingestions = {}
        self.queue = []
        self.lock = asyncio.Lock()
        self.processing_task = None

    def create_ingestion(self, request):
        ingestion_id = str(uuid4())
        created_time = time.time()
        batches = self._create_batches(request)
        self.ingestions[ingestion_id] = {
            "batches": batches,
            "status": "yet_to_start",
            "priority": request.priority,
            "created_time": created_time
        }
        for idx, batch in enumerate(batches):
            heapq.heappush(
                self.queue,
                (
                    PRIORITY_MAP[request.priority],
                    created_time,
                    ingestion_id,
                    idx
                )
            )
        if not self.processing_task or self.processing_task.done():
            self.processing_task = asyncio.create_task(self._process_batches())
        return ingestion_id

    def get_status(self, ingestion_id):
        ingestion = self.ingestions.get(ingestion_id)
        if not ingestion:
            return None
        batch_statuses = [b["status"] for b in ingestion["batches"]]
        if all(s == "yet_to_start" for s in batch_statuses):
            ingestion["status"] = "yet_to_start"
        elif all(s == "completed" for s in batch_statuses):
            ingestion["status"] = "completed"
        elif any(s == "triggered" for s in batch_statuses):
            ingestion["status"] = "triggered"
        return {
            "ingestion_id": ingestion_id,
            "status": ingestion["status"],
            "batches": [
                {
                    "batch_id": b["batch_id"],
                    "ids": b["ids"],
                    "status": b["status"]
                }
                for b in ingestion["batches"]
            ]
        }

    def _create_batches(self, request):
        batches = []
        for i in range(0, len(request.ids), BATCH_SIZE):
            batches.append({
                "batch_id": str(uuid4()),
                "ids": request.ids[i:i + BATCH_SIZE],
                "status": "yet_to_start"
            })
        return batches

    async def _process_batches(self):
        while self.queue:
            async with self.lock:
                priority, created_time, ingestion_id, batch_idx = heapq.heappop(self.queue)
                ingestion = self.ingestions[ingestion_id]
                batch = ingestion["batches"][batch_idx]
                if batch["status"] != "yet_to_start":
                    continue
                batch["status"] = "triggered"
            # Simulate external API call for each ID (1s per batch for demo)
            await asyncio.sleep(1)
            # Enforce 5s rate limit per batch
            await asyncio.sleep(4)
            async with self.lock:
                batch["status"] = "completed"

ingestion_store = IngestionStore()