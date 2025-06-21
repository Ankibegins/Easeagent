# APP/schemas/email.py

from pydantic import BaseModel, EmailStr

class Email(BaseModel):
    subject: str
    sender: EmailStr
    reciver: EmailStr
    body: str

class ReplyRequest(BaseModel):
    email_text: str

# APP/schemas/email_input.py


class EmailInput(BaseModel):
    message: str
