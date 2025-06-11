from fastapi import APIRouter

router = APIRouter()

@router.get("/user")
def get_user():
    return {"message": "Hello from the user route"}
