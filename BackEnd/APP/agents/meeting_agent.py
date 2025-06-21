import json
from pathlib import Path
from datetime import datetime, timedelta
from APP.schemas.meeting import Meeting

MEETING_FILE = Path("APP/data/meetings.json")
MEETING_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load/Save
def load_meetings():
    if MEETING_FILE.exists():
        with open(MEETING_FILE, "r") as f:
            return json.load(f)
    return []

def save_meetings(meetings):
    with open(MEETING_FILE, "w") as f:
        json.dump(meetings, f, indent=2)

# Suggest next available slot
def suggest_meeting_slot(profile, date):
    start = datetime.strptime(f"{date} {profile['preferred_meeting_hours']['start']}", "%Y-%m-%d %H:%M")
    end = datetime.strptime(f"{date} {profile['preferred_meeting_hours']['end']}", "%Y-%m-%d %H:%M")
    duration = timedelta(minutes=profile['default_meeting_duration_minutes'])
    
    existing = [
        m for m in load_meetings()
        if m["email"] == profile["email"] and m["date"] == date
    ]
    times_booked = {m["time"] for m in existing}

    current = start
    while current + duration <= end:
        t_str = current.strftime("%H:%M")
        if t_str not in times_booked:
            return t_str
        current += duration
    return None
