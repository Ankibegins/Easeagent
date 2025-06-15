from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

ai_router = APIRouter(prefix="/ai", tags=["AI Suggestions"])

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("⚠️ API key not found. Gemini will not work.")
    model = None
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    

# Input schema
class SuggestRequest(BaseModel):
    text: str  # Could be email, message, or task description

# Output route
@ai_router.post("/suggest")
def suggest_action(data: SuggestRequest):
    prompt = f"""
    Based on the following input, determine the user's intent and suggest a helpful action in structured JSON.

    Input: {data.text}

    Respond in this JSON format:
    {{
        "intent": "schedule_meeting / create_task / reply / ignore / escalate",
        "reason": "Why you think this intent",
        "action_suggestion": "What exactly to do"
    }}
    """

    try:
        response = model.generate_content(prompt)
        ai_response = response.text.strip()
        return {
            "message": "AI suggestion generated",
            "suggestion": ai_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
