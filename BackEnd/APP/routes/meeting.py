from fastapi import APIRouter, HTTPException
from APP.schemas.meeting import Meeting
from APP.agents.meeting_agent import load_meetings, save_meetings, suggest_meeting_slot
from APP.routes.user import load_business_profiles

meeting_router = APIRouter(prefix="/meetings", tags=["Meetings"])

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

@meeting_router.post("/")
def book_meeting(meeting: Meeting):
    meetings = load_meetings()
    meetings.append(meeting.dict())
    save_meetings(meetings)
    return {"message": "Meeting booked successfully!"}
