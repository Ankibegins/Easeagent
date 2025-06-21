# APP/routes/email.py

from fastapi import APIRouter, HTTPException
from APP.schemas.email import Email, ReplyRequest
from APP.agents.email_agent import send_email, get_all_emails
from APP.utils.gemini_connector import generate_email_reply

email_router = APIRouter(prefix="/emails", tags=["Emails"])

@email_router.get("/")
def fetch_emails():
    return {
        "message": "Emails fetched successfully",
        "emails": get_all_emails()
    }

@email_router.post("/")
def send_new_email(email: Email):
    stored_email = send_email(email.subject, email.sender, email.reciver, email.body)
    return {
        "message": "Email sent successfully!",
        "email": stored_email
    }

@email_router.post("/reply")
def reply_to_email(data: ReplyRequest):
    reply = generate_email_reply(data.email_text)
    return {
        "message": "Reply generated successfully!",
        "reply": reply
    }
