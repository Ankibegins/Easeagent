from fastapi import FastAPI
import json

from APP.routes.user import user_router
from APP.routes.task import task_router
from APP.routes.email import email_router
from APP.routes.ai import ai_router
from APP.routes.analytics import analytics_router 
from APP.routes.scheduler import scheduler_router
from APP.routes.ai_dispatch import ai_dispatch_router
from APP.routes.meetings import meeting_router




app = FastAPI()
app.include_router(meeting_router)
app.include_router(ai_dispatch_router)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(email_router)
app.include_router(ai_router)
app.include_router(analytics_router)
app.include_router(scheduler_router)

# Optional route for testing
@app.get("/")
def check():
    return {"message": "this is the main app"}
