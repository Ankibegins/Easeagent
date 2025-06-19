from datetime import datetime
from pathlib import Path
import json

SCHEDULE_FILE = Path("APP/data/schedule.json")

def load_schedule():
    if not SCHEDULE_FILE.exists():
        return []

    with open(SCHEDULE_FILE, "r") as f:
        return json.load(f)

def save_schedule(schedule):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedule, f, indent=2, default=str)

def schedule_event(description: str, event_time: datetime):
    event = {
        "description": description,
        "datetime": event_time.isoformat()
    }

    schedule = load_schedule()
    schedule.append(event)
    save_schedule(schedule)

    return event
