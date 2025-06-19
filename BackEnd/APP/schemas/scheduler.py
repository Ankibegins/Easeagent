from pydantic import BaseModel
from datetime import datetime

class ScheduleRequest(BaseModel):
    description: str
    datetime: datetime

class SchedulerEvent(BaseModel):
    description: str
    datetime: datetime
