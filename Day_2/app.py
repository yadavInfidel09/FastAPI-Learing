from fastapi import FastAPI , Depends , HTTPException , Header
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class PaginationParams:
    def __init__(self, skip: int = 0 , limit: int = 10):
        if limit > 100:
            raise HTTPException(
                status_code = 400 ,
                detail = "Limit cannot exceed 100"
            )
        self.skip = skip
        self.limit = limit


def verif_api_key( x_api_key : str = Header(...)):
    if x_api_key != "secret-key-123" :
        raise HTTPException(
            status_code = 403,
            detail = "invlaid API key"
        )
    return x_api_key

fake_users_db = {
    "token-abc": {"id": 1, "username": "utkarsh", "role": "admin"},
    "token-xyz": {"id": 2, "username": "john", "role": "viewer"},
}

def get_current_user( authorization : str = Header(...)):
    token = authorization.replace("Bearer ", "")
    user = fake_users_db.get(token)
    
    if not user:
        raise HTTPException(
            status_code = 401 ,
            detail = "Invalid token"
        )
    return user

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code = 403 ,
            detail = "Admin access required"
        )
    return current_user





@app.get("/itmes")
async def list_items(
    pagination : PaginationParams = Depends(PaginationParams)
):
    return {
        "skip": pagination.skip ,
        "limit": pagination.limit ,
        "items":[]
    }
    
    
@app.get("/protected")
async def protected_route(
    api_key: str = Depends( verif_api_key )
):
    return {"message": "You have access"}

@app.get("/profile")
async def get_profile(
    current_user: dict = Depends(get_current_user)
):
    return current_user

@app.delete("/admin/user/{user_id}")
async def delete_user(
    user_id : int , 
    admin : dict = Depends( require_admin )
):
    return {
        "message": f"User {user_id} deleted by {admin['username']}"
    }