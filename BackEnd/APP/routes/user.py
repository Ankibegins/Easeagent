from fastapi import APIRouter
user_router=APIRouter(tags=["users"])

prefix="/users"


@user_router.get("/")
def get_all_users():
    return{"messsage":"here is the list of all the users"}

@user_router.get("/{user_id}")
def get_user_by_id(user_id: int):
    return{"message":f"details of user with id {user_id}"}

