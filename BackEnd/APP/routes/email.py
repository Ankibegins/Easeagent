from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,EmailStr
from dotenv import load_dotenv
import google.generativeai as genai
import os

email_router = APIRouter(prefix="/emails", tags=["Emails"])

#l load api key from .env file
load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise HTTPException(status_code=500, detail="API key not found in environment variables")

if api_key:
    genai.configure(api_key=api_key)
    model=genai.GenerativeModel("gemini-2.0-flash")
else:
    model=None
    
email_db=[]
    
# Pydantic model for an Email
class email(BaseModel):
    subject:str
    sender:EmailStr
    reciver:EmailStr
    body:str

class reply_request(BaseModel):
    email_text: str



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
    
@email_router.post("/reply")
def generate_reply(data: reply_request):
    if not model:
        raise HTTPException(status_code=500, detail="Generative model is not configured")
    
    try:
        response = model.generate_content(
            prompt=f"Reply to this email: {data.email_text}",
            max_output_tokens=100,
            temperature=0.5
        )
        reply_text = response.candidates[0].content.strip()
        return {
            "message": "Reply generated successfully!",
            "reply": reply_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))