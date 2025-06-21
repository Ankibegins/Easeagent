from pydantic import BaseModel

class MeetingInput(BaseModel):
    message: str
