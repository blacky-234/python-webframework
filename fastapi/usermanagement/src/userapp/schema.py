from pydantic import BaseModel,EmailStr,Field,validator,ConfigDict
from typing import Optional
import re


class User(BaseModel):
    name: str = Field(min_length=5,max_length=50)
    email: EmailStr 
    phone: Optional[str] = None
    role: str = Field(default="user")
    status: bool = Field(default=True)

    @validator("phone")
    def validate_phone(cls, v):
        if v is None:
            return v
        v = re.sub(r"[^\d]", "", v)
        if not (10 <= len(v) <= 15):
            raise ValueError("Invalid phone number")
        return v


class UserCreate(User):
    password:str = Field(min_length=5,max_length=20, examples=["one upper and one lowercase letter and one number"])

    @validator("password")
    def password_complexity(cls,v):
        if len(v.encode("utf-8")) < 8:
            raise ValueError("Password should be at least 8 characters")
        if not any(char.isupper() for char in v):
            raise ValueError("Password should contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password should contain at least one lowercase letter")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password should contain at least one number")
        if not re.search(r"[!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/]", v):
            raise ValueError("Password should contain at least one special character")
        return v

class UserCreateResponse(BaseModel):
    message: str
    id: int

class UserListResponse(User):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserPaginationResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[UserListResponse]

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[bool] = None
    role: Optional[str] = None
