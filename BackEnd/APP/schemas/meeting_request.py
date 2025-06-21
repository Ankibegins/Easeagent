from pydantic import BaseModel

class MeetingRequest(BaseModel):
    request_text: str
