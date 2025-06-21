from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from APP.utils.gemini_connector import generate_email_reply
from APP.agents.inventory_agent import check_inventory
from APP.agents.scheduler_agent import schedule_event, load_schedule
from APP.agents.email_agent import send_email
from datetime import datetime
from dateparser import parse as parse_date
import json
import re

# Router setup
ai_dispatch_router = APIRouter(prefix="/ai", tags=["AI Dispatcher"])

# Request body schema
class DispatchRequest(BaseModel):
    email_text: str

# POST /ai/dispatch
@ai_dispatch_router.post("/dispatch")
def handle_dispatch(data: DispatchRequest):
    email_text = data.email_text

    # STEP 1: Craft prompt for Gemini
    prompt = f"""
    Analyze the following message and return an array of actions in clean JSON format only.
    
    Message: {email_text}

    Use this strict format:
    [
        {{
            "intent": "check_inventory / schedule_meeting / reply / ignore",
            "product": "pen",      # only if needed
            "quantity": 500,       # only if needed
            "datetime": "tomorrow 5pm"  # only if scheduling
        }}
    ]
    Do not include any explanation or preamble.
    """

    try:
        from APP.routes.ai import model  # Gemini model instance
        ai_response = model.generate_content(prompt)

        # 🔍 STEP 2: Extract raw text from Gemini response
        raw_text = ai_response.candidates[0].content.parts[0].text.strip()

        print("🔁 RAW GEMINI RESPONSE:", raw_text)  # Debugging

        # STEP 3: Extract JSON from Markdown block if exists
        match = re.search(r"```json\s*(.*?)\s*```", raw_text, re.DOTALL)
        response_text = match.group(1) if match else raw_text

        # STEP 4: Clean JSON formatting issues
        response_text = response_text.replace("'", '"')  # Fix single quotes

        # STEP 5: Parse the JSON
        intents = json.loads(response_text)

    except json.JSONDecodeError as decode_err:
        raise HTTPException(status_code=500, detail="Gemini JSON error: " + str(decode_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Gemini failed: " + str(e))

    actions = []

    # STEP 6: Loop through actions and process them
    for intent_data in intents:
        intent = intent_data.get("intent")

        if intent == "check_inventory":
            product = intent_data.get("product")
            quantity = intent_data.get("quantity", 0)
            inventory_result = check_inventory(product, quantity)
            actions.append({
                "type": "inventory_check",
                "product": product,
                "available": inventory_result
            })

        elif intent == "schedule_meeting":
            raw_time = intent_data.get("datetime")
            event_time = parse_date(raw_time)
            if not isinstance(event_time, datetime):
                actions.append({
                    "type": "schedule_meeting",
                    "status": "failed",
                    "reason": "Invalid date/time format"
                })
            else:
                existing_events = load_schedule()
                for event in existing_events:
                    if event["datetime"] == event_time.isoformat():
                        actions.append({
                            "type": "schedule_meeting",
                            "status": "conflict",
                            "reason": "Time already booked"
                        })
                        break
                else:
                    scheduled_event = schedule_event("Meeting from AI dispatch", event_time)
                    actions.append({
                        "type": "schedule_meeting",
                        "status": "scheduled",
                        "datetime": scheduled_event["datetime"]
                    })

        elif intent == "reply":
            reply = generate_email_reply(email_text)
            send_email(
                subject="Re: Automated Response",
                sender="assistant@easeagent.com",
                reciver="client@demo.com",  # Placeholder — replace with real email later
                body=reply
            )
            actions.append({
                "type": "reply_generated",
                "reply": reply
            })

        else:
            actions.append({
                "type": "unknown_or_ignored",
                "intent_data": intent_data
            })

    return {
        "message": "AI dispatch completed",
        "actions": actions
    }
