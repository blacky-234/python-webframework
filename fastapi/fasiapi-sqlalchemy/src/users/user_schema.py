from pydantic import BaseModel,EmailStr,Field,validator,ConfigDict
from typing import Optional

class UserSchema(BaseModel):
    username:str = Field(min_length=5,max_length=20, examples="hellojohns")
    email:EmailStr
    is_active:bool = True
    full_name: Optional[str] = Field(default=None, examples="John Doe")


class UserCreate(UserSchema):
    password:str = Field(min_length=5,max_length=20, examples="one upper and one lowercase letter and one number")

    @validator("password")
    def password_complexity(cls,v):
        # if len(v.encode("utf-8")) < 8:
        #     raise ValueError("Password should be at least 8 characters")
        # if not any(char.isupper() for char in v):
        #     raise ValueError("Password should contain at least one uppercase letter")
        # if not any(char.islower() for char in v):
        #     raise ValueError("Password should contain at least one lowercase letter")
        # if not any(char.isdigit() for char in v):
        #     raise ValueError("Password should contain at least one number")
        # return v
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password is too long (max 72 bytes)")
        return v

class UserResponse(UserSchema):
    id:int
    is_active:bool = True

    model_config = ConfigDict(from_attributes=True)
