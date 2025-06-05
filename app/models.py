from enum import Enum
from pydantic import BaseModel

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IngestionRequest(BaseModel):
    ids: list[int]
    priority: Priority