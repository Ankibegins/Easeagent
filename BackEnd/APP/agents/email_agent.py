import json
from pydantic import EmailStr
from typing import List
from APP.schemas.email import Email
from pathlib import Path

EMAIL_FILE = Path("APP/data/emails.json")
EMAIL_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

# Load emails from file
def load_emails() -> List[Email]:
    if EMAIL_FILE.exists():
        with open(EMAIL_FILE, "r") as f:
            emails_data = json.load(f)
            return [Email(**e) for e in emails_data]
    return []

# Save emails to file
def save_emails(emails: List[Email]):
    with open(EMAIL_FILE, "w") as f:
        json.dump([e.dict() for e in emails], f, indent=2)

# Send a new email
def send_email(subject: str, sender: EmailStr, reciver: EmailStr, body: str) -> Email:
    emails = load_emails()
    email = Email(subject=subject, sender=sender, reciver=reciver, body=body)
    emails.append(email)
    save_emails(emails)
    return email

# Fetch all emails
def get_all_emails() -> List[Email]:
    return load_emails()


from APP.routes.user import load_business_profiles
from APP.utils.gemini_connector import generate_email_reply  # ✅ Make sure this exists

def generate_email_reply(email: str, incoming_message: str) -> str:
    profiles = load_business_profiles()
    
    if email not in profiles:
        return "Business profile not found. Please set it up first."

    profile = profiles[email]
    
    prompt = f"""
You are a smart virtual assistant for the business "{profile['business_name']}", owned by {profile['owner_name']}.
Your working hours are {profile['preferred_meeting_hours']['start']} to {profile['preferred_meeting_hours']['end']}.
You can schedule up to {profile['max_meetings_per_day']} meetings per day, each lasting {profile['default_meeting_duration_minutes']} minutes.

Here’s a new customer email. Generate a friendly, professional reply that fits the context:
---
{incoming_message}
---
"""

    return generate_email_reply(prompt)
