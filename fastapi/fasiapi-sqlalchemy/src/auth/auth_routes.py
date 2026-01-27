from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth.auth_service import AuthService
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

auth = APIRouter(prefix="/auth",tags=["auth"], responses={404: {"description": "Not found"}})


@auth.post("/login",status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:AsyncSession = Depends(get_db)):
    """
    This ONLY accepts application/x-www-form-urlencoded, NOT JSON.
    """

    auth = AuthService(db)
    user = await auth.authenticate(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = await auth.login(user)

    
    return {"access_token": token, "token_type": "bearer"}