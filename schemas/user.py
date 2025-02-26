from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    agent = "agent"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.agent


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
