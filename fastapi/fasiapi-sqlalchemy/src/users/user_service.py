from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import user_models,user_schema
from sqlalchemy.exc import IntegrityError
from src.core.password_utility import get_password_hash

class UsernameAlreadyExists(Exception):
    pass

class EmailAlreadyExists(Exception):
    pass


class UserService:
    def __init__(self,db:AsyncSession):
        self.db = db

    async def get_by_id(self,user_id:int)-> user_models.User | None:
        result = await self.db.execute(select(user_models.User).where(user_models.User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self,email:str)-> user_models.User | None:
        result = await self.db.execute(select(user_models.User).where(user_models.User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self,username:str)-> user_models.User | None:
        result = await self.db.execute(select(user_models.User).where(user_models.User.username == username))
        return result.scalar_one_or_none()

    async def list(self,skip:int=0,limit:int=100)-> list[user_models.User]:
        result = await self.db.execute(select(user_models.User).offset(skip).limit(limit)).scalars().all()
        return result
    
    async def create(self,user: user_schema.UserCreate)-> user_models.User:
        hashed_password = get_password_hash(user.password)
        if await self.get_by_username(user.username):
            raise UsernameAlreadyExists
        if await self.get_by_email(user.email):
            raise EmailAlreadyExists
        db_user = user_models.User(username=user.username,email=user.email,password=hashed_password,full_name=user.full_name)
        self.db.add(db_user)
        try:
            await self.db.commit()
            await self.db.refresh(db_user)
        except IntegrityError:
            await self.db.rollback()
            raise
        return db_user
