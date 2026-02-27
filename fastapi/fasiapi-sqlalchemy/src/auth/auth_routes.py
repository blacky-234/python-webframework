from fastapi import APIRouter, Depends, HTTPException, status,Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth.auth_service import AuthService,get_auth_service
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

auth = APIRouter(prefix="/auth",tags=["auth"], responses={404: {"description": "Not found"}})


@auth.post("/login",status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),auth_service:AuthService = Depends(get_auth_service)):
    """
    This ONLY accepts application/x-www-form-urlencoded, NOT JSON.
    """

    user = await auth_service.authenticate(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = await auth_service.login(user)
    return {"access_token": token, "token_type": "bearer"}

@auth.post("/refresh-token")
async def refresh_token(refresh_token: str = Body(...),auth_service:AuthService = Depends(get_auth_service)):
    pass