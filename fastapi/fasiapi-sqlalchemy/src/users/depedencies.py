# users/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import UserRepository
from .user_service import UserService

def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)
