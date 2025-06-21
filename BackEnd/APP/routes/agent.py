from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from APP.schemas.email_input import EmailInput
from APP.utils.gemini_connector import generate_email_reply
agent_router = APIRouter(prefix="/agents", tags=["Agents"])

# In-memory agent database (temporary, until DB integration)
agent_db = []

# Schema for AI Agent
class Agent(BaseModel):
    name: str                     # e.g., "ReplyBot", "Scheduler", "Summarizer"
    role: str                     # e.g., "Handles email replies"
    capabilities: List[str]       # e.g., ["reply to emails", "summarize text"]

# ------------------- AGENT CRUD -------------------

@agent_router.get("/")
def get_agents():
    return {
        "message": "Agents fetched successfully!",
        "agents": agent_db
    }

@agent_router.get("/{agent_id}")
def get_agent(agent_id: int):
    if agent_id < 0 or agent_id >= len(agent_db):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {
        "message": "Agent found",
        "agent": agent_db[agent_id]
    }

@agent_router.post("/")
def add_agent(agent: Agent):
    agent_db.append(agent)
    return {
        "message": "Agent added successfully!",
        "agent": agent
    }

@agent_router.put("/{agent_id}")
def update_agent(agent_id: int, updated_agent: Agent):
    if agent_id < 0 or agent_id >= len(agent_db):
        raise HTTPException(status_code=404, detail="Agent not found")
    agent_db[agent_id] = updated_agent
    return {
        "message": "Agent updated successfully!",
        "agent": updated_agent
    }

@agent_router.delete("/{agent_id}")
def delete_agent(agent_id: int):
    if agent_id < 0 or agent_id >= len(agent_db):
        raise HTTPException(status_code=404, detail="Agent not found")
    deleted = agent_db.pop(agent_id)
    return {
        "message": "Agent deleted successfully!",
        "deleted_agent": deleted
    }

# ------------------- EMAIL REPLY -------------------

@agent_router.post("/email-reply")
def get_ai_email_reply(email: EmailInput):
    try:
        reply = generate_email_reply(email.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate reply: {e}")
