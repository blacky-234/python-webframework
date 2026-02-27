from fastapi import APIRouter,status,Depends,HTTPException,Query,Body,Response,Request
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Database import init_db
from . import schema
from .service import UserService,EmailAlreadyExists,DataLimitation,UserNotFoundException,TokenManagementService
from utility.tokenManagement import InvalidToken,Tokens
from jose import jwt,JWTError
from jose.exceptions import ExpiredSignatureError
import asyncio
from datetime import datetime,timedelta,timezone



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def authorization(token: str = Depends(oauth2_scheme)):
    payload = Tokens.token_payload(token)    
    return payload



user = APIRouter(
    prefix="",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)



@user.get("/")
async def root():
    return {"message": "Hello World body motions"}

@user.post("/refresh-token",status_code=status.HTTP_200_OK)
async def refresh_token(request: Request,db:Session=Depends(init_db)):
    """Create an endpoint that clients call to exchange a valid refresh token for a new access token."""
    try:
        refresh_t = request.cookies.get('refresh_token')
        if refresh_t is None:
            raise InvalidToken()
        
        #TODO: remove paloaded no need 
        
        payload_task = asyncio.to_thread(Tokens.token_payload,refresh_t)
        token_task = asyncio.to_thread(TokenManagementService,db)
        payload,token_service = await asyncio.gather(payload_task,token_task)

        if token_service:
            #TODO: user expiry time checking
            access_token_expiry = timedelta(minutes=15)
            access_token = Tokens.create_access_token(payload,access_token_expiry)

            # print(f"what is payload ---->Service----> {payload}")
            return {"access_token": access_token,"token_type": "bearer",}
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid Refresh token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@user.post("/auth/login",status_code=status.HTTP_200_OK)
async def login(response: Response,formdata:OAuth2PasswordRequestForm=Depends(),
                db:Session=Depends(init_db)):
    try:
        service = UserService(db)
        user = await service.authenticate(formdata.username,formdata.password)
        if user is not None:
            token = await service.login(user)
            response.set_cookie(
                key="refresh_token",
                value=token["refresh_token"],
                httponly=True,
                secure=False,
                max_age=7 * 24 * 60 * 60,
                samesite="lax",
                expires=token["expiry_at"],
                path="/"
            )
            return {"access_token":token["access_token"],"token_type":"bearer"}
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")
    except Exception as e:
        print(e)
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
async def get_users(auth_user:dict=Depends(authorization),db:Session=Depends(init_db),page:int=Query(1,ge=1),limit:int=Query(20,ge=1)):

    try:
        service = UserService(db)
        validate = await service.validate_by_email_id(auth_user["email"],auth_user["id"])
        if validate is None:
            raise UserNotFoundException()
        if validate.role != "admin":
            raise UserNotFoundException()
        result = await service.get_all_users(page=page,limit=limit)
        return result
    except DataLimitation as e:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Page {page} does not exist. Total pages: {e.total_pages}")
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@user.delete('/users/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:int,auth_user:dict=Depends(authorization),db:Session=Depends(init_db)):
    try:
        service = UserService(db)
        validate = await service.validate_by_email_id(auth_user["email"],auth_user["id"])
        if validate is None:
            raise UserNotFoundException()
        if validate.role != "admin":
            raise UserNotFoundException()
        await service.delete_user(id)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@user.get('/users/{id}',response_model=schema.UserListResponse,status_code=status.HTTP_200_OK)
async def get_user_profile(id:int,db:Session=Depends(init_db)):
    try:
        service = UserService(db)
        result = await service.get_by_id(id)
        return result
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@user.patch('/users/{id}',status_code=status.HTTP_200_OK)
async def update_user_profile(id:int,user:schema.UserUpdate,auth_user:dict=Depends(authorization),db:Session=Depends(init_db)):
    try:
        service = UserService(db)
        validate = await service.validate_by_email_id(auth_user["email"],auth_user["id"])
        if validate is None:
            raise UserNotFoundException()
        await service.user_update(id,user,role=validate.role)
        return {"message":"User updated successfully"}
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@user.get('/auth/me',response_model=schema.UserListResponse,status_code=status.HTTP_200_OK)
async def authorization_profile(auth_user:dict=Depends(authorization),db:Session=Depends(init_db)):
    try:
        service = UserService(db)
        result = await service.get_by_id(auth_user["id"])
        return result
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))