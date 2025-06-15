from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

agent_router = APIRouter(prefix="/agents", tags=["Agents"])

# In-memory agent database
agent_db = []

# Pydantic model for an AI Agent
class Agent(BaseModel):
    name: str             # e.g., "ReplyBot", "Scheduler", "Summarizer"
    role: str             # What it does, e.g., "Handles email replies"
    capabilities: List[str]  # List of things this agent can do

# GET all agents
@agent_router.get("/")
def get_agents():
    return {
        "message": "Agents fetched successfully!",
        "agents": agent_db
    }

# GET single agent by index
@agent_router.get("/{agent_id}")
def get_agent(agent_id: int):
    if agent_id < 0 or agent_id >= len(agent_db):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {
        "message": "Agent found",
        "agent": agent_db[agent_id]
    }

# POST add a new agent
@agent_router.post("/")
def add_agent(agent: Agent):
    agent_db.append(agent)
    return {
        "message": "Agent added successfully!",
        "agent": agent
    }

# PUT update agent by index
@agent_router.put("/{agent_id}")
def update_agent(agent_id: int, updated_agent: Agent):
    if agent_id < 0 or agent_id >= len(agent_db):
        raise HTTPException(status_code=404, detail="Agent not found")
    agent_db[agent_id] = updated_agent
    return {
        "message": "Agent updated successfully!",
        "agent": updated_agent
    }

# DELETE remove agent
@agent_router.delete("/{agent_id}")
def delete_agent(agent_id: int):
    if agent_id < 0 or agent_id >= len(agent_db):
        raise HTTPException(status_code=404, detail="Agent not found")
    deleted = agent_db.pop(agent_id)
    return {
        "message": "Agent deleted successfully!",
        "deleted_agent": deleted
    }
