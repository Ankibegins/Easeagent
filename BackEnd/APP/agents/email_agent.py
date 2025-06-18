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
