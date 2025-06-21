from pydantic import BaseModel, EmailStr
from typing import Optional

class Meeting(BaseModel):
    email: EmailStr
    date: str  # e.g., "2025-06-22"
    time: str  # e.g., "15:00"
    topic: Optional[str] = None
