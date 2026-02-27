from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import user_models

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(user_models.User).where(user_models.User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str):
        result = await self.db.execute(
            select(user_models.User).where(user_models.User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str):
        result = await self.db.execute(
            select(user_models.User).where(user_models.User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, user: user_models.User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
