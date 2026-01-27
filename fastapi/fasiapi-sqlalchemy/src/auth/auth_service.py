from sqlalchemy.ext.asyncio import AsyncSession
from src.users.user_service import UserService
from src.core.password_utility import verify_password
from src.users import user_models
from authentication import Tokens
from datetime import datetime, timedelta



class AuthService(UserService):

    def __init__(self,db:AsyncSession):
        self.db = db
        super().__init__(db)


    async def authenticate(self,username: str, password: str)-> user_models.User | None:

        user = await self.get_by_username(username)
        if not user or not verify_password(password,user.password):
            return None
            # raise IncorrectUserNamePassword()        
        return user


    async def login(self,user:user_models.User)->UserService:

        data = {
            "username":user.username,}

        token = Tokens.create_access_token(data,expires_delta=timedelta(minutes=30))
        
        return token


class IncorrectUserNamePassword(Exception):
    def __init__(self):
        super().__init__("Incorrect username or password")