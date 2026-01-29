from sqlalchemy.ext.asyncio import AsyncSession
from src.users.user_service import UserService
from src.core.password_utility import verify_password
from src.users import user_models
from authentication import Tokens
from datetime import datetime, timedelta
import auth_models



class AuthService(UserService):

    def __init__(self,db:AsyncSession):
        self.db = db
        self.access_token = 15
        self.refresh_token = 7
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
        
        access_token_expires = timedelta(minutes=self.access_token)
        refresh_token_expires = timedelta(days=self.refresh_token)



        acc_token = Tokens.create_access_token(data,access_token_expires)
        ref_token = Tokens.create_refresh_token(data,refresh_token_expires)

        token = auth_models.TokenManagement(
            user_id=user.id,
            refresh_token=ref_token,
            expires_at=datetime.utcnow() + refresh_token_expires)
        self.db.add(token)
        self.db.commit()
        return {"access_token":acc_token,"refresh_token":ref_token,"token_type":"bearer"}


class IncorrectUserNamePassword(Exception):
    def __init__(self):
        super().__init__("Incorrect username or password")