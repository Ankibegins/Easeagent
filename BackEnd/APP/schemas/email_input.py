from pydantic import BaseModel

class EmailInput(BaseModel):
    message: str
