from fastapi import APIRouter
from APP.agents.task_agent import run_task_flow

task_router = APIRouter(prefix="/task", tags=["Task"])

@task_router.post("/run_task_flow")
def run_flow():
    results =run_task_flow()
    return {
        "message":"task flow executed successfully",
        "results": results
    }
    
