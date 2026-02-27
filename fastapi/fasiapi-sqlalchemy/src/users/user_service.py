"""
Application Layer 

"""
from .repository import UserRepository
from .exception import UsernameAlreadyExists, EmailAlreadyExists
from src.core.password_utility import get_password_hash
from . import user_models, user_schema

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user: user_schema.UserCreate):
        if await self.repo.get_by_username(user.username):
            raise UsernameAlreadyExists()

        if await self.repo.get_by_email(user.email):
            raise EmailAlreadyExists()

        hashed_password = get_password_hash(user.password)

        db_user = user_models.User(
            username=user.username,
            email=user.email,
            password=hashed_password,
            full_name=user.full_name
        )

        return await self.repo.create(db_user)
