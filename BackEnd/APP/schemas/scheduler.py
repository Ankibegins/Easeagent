from pydantic import BaseModel
from datetime import datetime

class SchedulerRequest(BaseModel):
    description: str

class SchedulerResponse(BaseModel):
    description: str
    datetime: datetime
