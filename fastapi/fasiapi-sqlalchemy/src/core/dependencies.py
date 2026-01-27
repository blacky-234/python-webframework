from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from authentication import Tokens
from auth.auth_schema import TokenData
from users.user_service import UserService
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credential_exceptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = Tokens.verify_access_token(token)
    if token_data is None or token_data.username is None:
        raise credential_exceptions
    user = UserService(db).get_by_username(token_data.username)
    if user is None:
        raise credential_exceptions
    #TODO: is_active handles
    return user