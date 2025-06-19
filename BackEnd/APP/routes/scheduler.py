from fastapi import APIRouter, HTTPException
from APP.agents.scheduler_agent import schedule_event, load_schedule
from APP.schemas.scheduler import ScheduleRequest

scheduler_router = APIRouter(prefix="/scheduler", tags=["scheduler"])

@scheduler_router.post("/")
def create_schedule(request: ScheduleRequest):
    try:
        event = schedule_event(request.description, request.datetime)
        return {"message": "Event scheduled", "event": event}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@scheduler_router.get("/")
def get_schedule():
    schedule = load_schedule()
    return {"message": "Scheduled events retrieved", "events": schedule}
