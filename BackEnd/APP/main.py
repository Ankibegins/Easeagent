from fastapi import FastAPI
from APP.routes.user import user_router
from APP.routes.task import task_router
from APP.routes.email import email_router

app= FastAPI()
app.include_router(user_router)
app.include_router(task_router)
app.include_router(email_router)
 
def check():
    return{"message":"this is the main app"}