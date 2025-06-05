from datetime import datetime
from heapq import heappush, heappop
import asyncio
from .config import RATE_LIMIT, BATCH_SIZE

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._lock = asyncio.Lock()
    
    async def add_batch(self, priority, created_at, batch):
        async with self._lock:
            heappush(self._queue, (-priority.value, created_at.timestamp(), batch))

    async def get_next_batch(self):
        async with self._lock:
            return heappop(self._queue) if self._queue else None

queue = PriorityQueue()
last_processed = datetime.min

async def add_to_queue(batch):
    await queue.add_batch(batch.priority, batch.created_at, batch)

async def process_batches():
    global last_processed
    while True:
        now = datetime.now()
        if (now - last_processed).total_seconds() >= RATE_LIMIT:
            next_batch = await queue.get_next_batch()
            if next_batch:
                _, _, batch = next_batch
                await process_batch(batch)
                last_processed = datetime.now()
        await asyncio.sleep(1)