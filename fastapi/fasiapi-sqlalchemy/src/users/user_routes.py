from typing import Optional
from fastapi import APIRouter, Depends, HTTPException,Query,status
from . import user_schema
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .user_service import UserService,UsernameAlreadyExists,EmailAlreadyExists

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("/", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: user_schema.UserCreate,db:AsyncSession = Depends(get_db)):
    try:
        user_service = UserService(db)
        result = await user_service.create(user_in)
        return result
    except UsernameAlreadyExists:
        raise HTTPException(status_code=400, detail="Username already registered")
    except EmailAlreadyExists:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_router.get("/get")
def read_users():
    return [{"name": "Foo"}, {"name": "Bar"}]


"""
TODO:Database connection Router configured
user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_db)]
)
"""

# @user_router.get("/{user_id}", response_model=UserSchema)
# async def read_users(user_id:int,service:UserService = Depends()):
#     user = service.get_user(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return [{"name": "Foo"}, {"name": "Bar"}]

# @user_router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserSchema):
#     return user

# @user_router.delete("/{user_id}", response_model=UserSchema,status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(user_id: int, user: UserSchema):
#     return user


# #Query parameter call using 
# @user_router.get("/name/{uid}")
# async def names(uid:int,q:Optional[str] =None):
#     a ={"uid":uid}
#     return a