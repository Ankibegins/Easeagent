from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from fastapi import Body
import random
import os
import json  # ✅ ADDED: to use load/save for JSON
from pathlib import Path  # ✅ ADDED: to define user file path

user_router = APIRouter(prefix="/users", tags=["users"])
load_dotenv()

# ✅ DELETED: old `send_email()` import – now using real email with FastMail
# ❌ from APP.agents.email_agent import send_email

# File where users are stored
USER_FILE = Path("APP/data/users.json")
USER_FILE.parent.mkdir(parents=True, exist_ok=True)  # ✅ ADDED: ensure dir exists

# OTP memory store (not persisted)
otp_store = {}

# ✅ Real email configuration using environment variables
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

# Load users from JSON
def load_users():
    if USER_FILE.exists():
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    return []

# Save users to JSON
def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Input model
class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr

@user_router.post("/register")
async def register_user(data: RegisterRequest):
    users = load_users()

    for user in users:
        if user["username"] == data.username:
            raise HTTPException(status_code=400, detail="Username already exists")
        if user["email"] == data.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    # ✅ Generate 4-digit verification code
    code = str(random.randint(1000, 9999))

    # ✅ SEND EMAIL USING FASTMAIL
    message = MessageSchema(
        subject="EaseAgent Email Verification Code",
        recipients=[data.email],
        body=f"Your verification code is: {code}",
        subtype="plain"
    )
    try:
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    # ✅ Create user object with `is_verified` False
    new_user = {
        "username": data.username,
        "password": data.password,
        "email": data.email,
        "is_verified": False,
        "verification_code": code
    }

    users.append(new_user)
    save_users(users)

    return {"message": "User registered. Verification code sent to the email."}


from fastapi import Body

class VerifyRequest(BaseModel):
    email: EmailStr
    code: str

@user_router.post("/verify")
def verify_email(data: VerifyRequest):
    users = load_users()
    user_found = False

    for user in users:
        if user["email"] == data.email:
            user_found = True
            if user["is_verified"]:
                return {"message": "User already verified."}
            if user.get("verification_code") == data.code:
                user["is_verified"] = True
                user["verification_code"] = None
                save_users(users)
                return {"message": "Email verified successfully!"}
            else:
                raise HTTPException(status_code=400, detail="Incorrect verification code.")

    if not user_found:
        raise HTTPException(status_code=404, detail="User not found.")
    
class LoginRequest(BaseModel):
    username: str
    password: str

@user_router.post("/login")
def login_user(data: LoginRequest):
    users = load_users()

    for user in users:
        if user["username"] == data.username:
            if user["password"] != data.password:
                raise HTTPException(status_code=401, detail="Incorrect password")
            if not user["is_verified"]:
                raise HTTPException(status_code=403, detail="Email not verified")
            return {"message": "Login successful", "username": user["username"], "email": user["email"]}

    raise HTTPException(status_code=404, detail="User not found")


# 🔧 For business setup
BUSINESS_PROFILE_FILE = Path("APP/data/business_profiles.json")
BUSINESS_PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_business_profiles():
    if BUSINESS_PROFILE_FILE.exists():
        with open(BUSINESS_PROFILE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_business_profiles(profiles):
    with open(BUSINESS_PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)


from typing import Optional,Dict

class TimeRange(BaseModel):
    start: str
    end:str

class BusinessSetupRequest(BaseModel):
    email: EmailStr
    business_name: str
    owner_name: str
    preferred_meeting_hours: dict
    max_meetings_per_day: int
    default_meeting_duration_minutes: int


@user_router.post("/setup")
def setup_business_profile(data:BusinessSetupRequest):
    users=load_users()
    profiles=load_business_profiles()    

    user = next((u for u in users if u["email"].lower() == data.email.lower()), None)

    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    if not user.get("is_verified"):
        raise HTTPException(status_code=403,detail="email not verified")
    
    if data.email in profiles:
        raise HTTPException(status_code=400,detail="setup already coompleted")
    profiles[data.email]=data.dict()
    save_business_profiles(profiles)
    
    return {"message":"business setup completed successfully"}

from fastapi import Query

@user_router.get("/profile")
def get_business_profile(email: EmailStr = Query(...)):
    users = load_users()
    profiles = load_business_profiles()

    # Check if user exists and is verified
    user = next((u for u in users if u["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.get("is_verified"):
        raise HTTPException(status_code=403, detail="Email not verified")

    profile = profiles.get(email)
    if not profile:
        raise HTTPException(status_code=404, detail="Business profile not found")

    return {"profile": profile}
