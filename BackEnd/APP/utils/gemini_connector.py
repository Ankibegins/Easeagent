import google.generativeai as genai
import os
import json
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


# ---------------------------------------------
# ✅ Email Reply Generator (Already Working)
# ---------------------------------------------
def generate_email_reply(email_text: str) -> str:
    """
    Generate a reply using Gemini AI for the given email text.
    """
    try:
        response = model.generate_content(f"Reply to this email in a polite and professional tone: {email_text}")
        return response.text.strip() if hasattr(response, "text") else "No reply generated."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")


# ---------------------------------------------
# 🧠 Meeting Request Parser (New!)
# ---------------------------------------------
def parse_meeting_request(email_text: str) -> dict:
    prompt = (
        "You are a meeting assistant. Extract the following information from the message:\n"
        "- date (in YYYY-MM-DD format)\n"
        "- time (in HH:MM, 24-hour format)\n"
        "- topic\n"
        "- email (optional)\n\n"
        f"Message: \"{email_text}\"\n\n"
        "Return ONLY a valid JSON object with the keys: date, time, topic, and email.\n"
        "Example:\n"
        '{ "date": "2025-06-22", "time": "15:00", "topic": "EaseAgent discussion", "email": "optional@email.com" }'
    )

    try:
        response = model.generate_content(prompt)
        print("🔍 Gemini Raw Output:\n", response.text)  # ✅ Debug print
        # Clean markdown code blocks if present
        cleaned = (
            response.text.strip()
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Gemini meeting parse error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
