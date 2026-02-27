from pydantic import BaseModel,EmailStr,Field,validator,ConfigDict,constr,field_validator
from typing import Optional
import re
from datetime import datetime 

class UserSchema(BaseModel):
    username:str = constr(min_length=3,max_length=50,strip_whitespace=True)
    email:EmailStr
    is_active:bool = True
    full_name: Optional[str] = Field(default=None, examples=["John Doe"])

    @field_validator("username",mode="before")
    @classmethod
    def normalize_username(cls, v: str) -> str:
        return v.lower().strip()



class UserCreate(UserSchema):
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
        

class UserResponse(UserSchema):
    id:int
    is_active:bool = True
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)
