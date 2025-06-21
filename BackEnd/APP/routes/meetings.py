from fastapi import APIRouter, HTTPException
from APP.schemas.meeting import Meeting
from APP.schemas.meeting_input import MeetingInput
from APP.agents.meeting_agent import load_meetings, save_meetings, suggest_meeting_slot
from APP.routes.user import load_business_profiles
from APP.utils.gemini_connector import parse_meeting_request

meeting_router = APIRouter(prefix="/meetings", tags=["Meetings"])

# ✅ GET next available time slot for a given date and email
@meeting_router.get("/{email}/{date}")
def get_next_available_slot(email: str, date: str):
    profiles = load_business_profiles()
    profile = profiles.get(email)
    if not profile:
        raise HTTPException(status_code=404, detail="Business profile not found")

    slot = suggest_meeting_slot(profile, date)
    if not slot:
        raise HTTPException(status_code=400, detail="No available slots for this day")

    return {"suggested_time": slot}

# ✅ POST book a meeting manually
@meeting_router.post("/")
def book_meeting(meeting: Meeting):
    meetings = load_meetings()
    meetings.append(meeting.dict())
    save_meetings(meetings)
    return {"message": "Meeting booked successfully!"}

# ✅ POST parse meeting info from user message using Gemini
@meeting_router.post("/parse-request")
def parse_meeting_request_route(message: MeetingInput):
    try:
        data = parse_meeting_request(message.message)
        return {
            "message": "Meeting info extracted successfully!",
            "meeting_details": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
