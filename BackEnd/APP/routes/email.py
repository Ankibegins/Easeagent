from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,EmailStr

# Pydantic model for an Email
class email(BaseModel):
    subject:str
    sender:EmailStr
    reciver:EmailStr
    body:str

email_router = APIRouter(prefix="/emails", tags=["Emails"])

email_db=[]

@email_router.get("/")
def get_emails():
    return {
        "message":"emails fetched successfully",
        "emails":email_db
    }
    
# POST route to send an email    
@email_router.post("/")
def send_email(email: email):
    email_db.append(email)
    return {
        "message": "Email sent successfully!",
        "email": email
    }