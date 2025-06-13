from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Pydantic model for a Task
class Task(BaseModel):
    title: str
    description: str
    
task_db=[]

# GET route
@task_router.get("/")
def get_tasks():
    return {"message": "tasks are fetched successfully!",
            "tasks":task_db}




# POST route
@task_router.post("/")
def create_task(task: Task):
    task_db.append(task)
    return {
        
        "message": "Task created successfully!",
        "task": task
    }

# put updating a task by index
@task_router.put("/{task_id}")
def update_task(task_id:int,updated_task: Task):
    if task_id < 0 or task_id >= len(task_db):
        raise HTTPException(status_code=404, detail="task not found")
    task_db[task_id]= updated_task
    return {
        "message": "task updated successfully!",
        "task": updated_task
    }
    
# DELETE route to delete a task by index
@task_router.delete("/{task_id}")
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(task_db):
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = task_db.pop(task_id)
    return {
        "message": "Task deleted successfully!",
        "deleted_task": deleted_task
    }

    
