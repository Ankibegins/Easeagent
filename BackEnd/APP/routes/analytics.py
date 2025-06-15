from fastapi import APIRouter
from APP.routes.email import email_db
from APP.routes.agent import agent_db
from APP.routes.task import task_db

analytics_router =APIRouter(prefic="/analytics", tags=["Analytics"])


@analytics_router.get("/emails")
def get_email_stats():
    return {
        "message": "Email statistics fetched successfully",
        "total_emails": len(email_db),
    }
    
    
    
@analytics_router.get("/agents")
def get_agent_stats():
    return {
        "message": "Agent statistics fetched successfully",
        "total_agents": len(agent_db),
    }
    
    
@analytics_router.get("/tasks")
def get_task_stats():
   
        total= len(task_db),
        completed= len([task for task in task_db if task.get("status") == "completed"]),
        pending=total-completed,
        return {
        "message": "Task statistics fetched successfully",
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending
    }