from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from enum import Enum
from datetime import datetime


app = FastAPI()

class UserRole( str , Enum):
    admin = "admin"
    developer = "devloper"
    viewer = "viewer"

class CreateUserRequest(BaseModel):
    username: str = Field( min_length = 3 , max_length=30 )
    email: str
    phone_number : str
    password: str = Field( min_length=8)
    confirm_password: str
    role: UserRole = UserRole.developer
    age: Optional[int] = Field( default=None , ge=13, le=120)
    website : str
    
    @field_validator('website')
    @classmethod
    def email_must_start(cls ,v):
        if not v.startswith('https://'):
            raise ValueError('Website must start with http://')
        
    
    @field_validator('email')
    @classmethod
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        
        if v.split('@')[1] == 'tempmail.com':
            raise ValueError('Disposable emails not allowed')
        
        return v.lower()
    
    @field_validator('phone_number')
    @classmethod
    def ph_must_startwith(cls, v):
        if not v.startswith('+91'):
            raise ValueError('PhoneNumber must start with +91')
        
    
    @model_validator(mode='after')
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self
    
class UserResponse(BaseModel):
    id: int
    username: str
    email:str
    role: UserRole
    created_at: datetime
    
@app.post("/users", response_model= UserResponse )
async def creatre_user(user: CreateUserRequest):
    return UserResponse(
        id = 1,
        username = user.username,
        email = user.email,
        role = user.role,
        created_at = datetime.now()
    )