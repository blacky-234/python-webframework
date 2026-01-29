from fastapi import APIRouter,status,Depends,HTTPException,Query
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Database import init_db
from . import schema
from .service import UserService,EmailAlreadyExists,DataLimitation,UserNotFoundException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



user = APIRouter(
    prefix="",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)



@user.get("/")
async def root():
    return {"message": "Hello World body motions"}

@user.post("/auth/login",status_code=status.HTTP_200_OK)
async def login(formdata:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(init_db)):
    try:
        service = UserService(db)
        user = await service.authenticate(formdata.username,formdata.password)
        if user is not None:
            token = await service.login(user)
            return token
        return {"message":"User logged in successfully"}
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@user.post('/auth/register',response_model=schema.UserCreateResponse,status_code=status.HTTP_201_CREATED)
async def register(user:schema.UserCreate,db:Session=Depends(init_db),token: str = Depends(oauth2_scheme)):
    print(f"What is token --------> {token}")
    try:
        service = UserService(db)
        result  = await service.create_user(user)
        return {"message":"User created successfully","id":result.id}
    except EmailAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@user.get('/users',response_model=schema.UserPaginationResponse,status_code=status.HTTP_200_OK)
async def get_users(db:Session=Depends(init_db),page:int=Query(1,ge=1),limit:int=Query(20,ge=1)):

    #TODO: (admin only) based on role
    try:
        service = UserService(db)
        result = await service.get_all_users(page=page,limit=limit)
        return result
    except DataLimitation as e:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Page {page} does not exist. Total pages: {e.total_pages}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@user.delete('/users/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:int,db:Session=Depends(init_db)):
    #TODO: (admin only)
    try:
        service = UserService(db)
        await service.delete_user(id)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@user.get('/users/{id}',response_model=schema.UserListResponse,status_code=status.HTTP_200_OK)
async def get_user_profile(id:int,db:Session=Depends(init_db)):
    #TODO: (admin only or same user)
    try:
        service = UserService(db)
        result = await service.get_by_id(id)
        return result
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@user.patch('/users/{id}',status_code=status.HTTP_200_OK)
async def update_user_profile(id:int,user:schema.UserUpdate,db:Session=Depends(init_db)):
    #TODO: (admin only or same user)
    try:
        service = UserService(db)
        await service.user_update(id,user)
        return {"message":"User updated successfully"}
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    