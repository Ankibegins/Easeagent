import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise HTTPException(status_code=500, detail="API key not found")

# Configure Gemini once
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_email_reply(email_text: str) -> str:

    """
    Generate a reply using Gemini AI for the given email text.
    """
    try:
        response = model.generate_content(f"Reply to this email in a polite and professional tone: {email_text}")
        return response.text.strip() if hasattr(response, "text") else "No reply generated."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
