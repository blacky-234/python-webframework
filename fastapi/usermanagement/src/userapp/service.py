from math import ceil
from sqlalchemy.orm import Session
from . import models
from . import schema
from utility.password import password_hash,verify_password
from datetime import datetime,timedelta,timezone
from utility.tokenManagement import Tokens,InvalidToken


class EmailAlreadyExists(Exception):
    pass
class DataLimitation(Exception):
    def __init__(self, total_pages: int):
        self.total_pages = total_pages

class UserNotFoundException(Exception):
    pass

class UserService:

    def __init__(self,db:Session):
        self.db = db
        self.access_token = 15
        self.refresh_token = 7
    
    async def login(self,user:models.User):
        data = {
            "id":user.id,
            "username":user.name,
            "email":user.email,
            "role":user.role
            }
        
        access_token_expires = timedelta(minutes=self.access_token)
        refresh_token_expires = timedelta(days=self.refresh_token)



        acc_token = Tokens.create_access_token(data,access_token_expires)
        ref_token = Tokens.create_refresh_token(data,refresh_token_expires)
        # expiry_at = datetime.utcnow() + refresh_token_expires
        expiry_at = datetime.now(timezone.utc)+refresh_token_expires
        token = models.TokenManagement(
            user_id=user.id,
            refresh_token=ref_token,
            expires_at=expiry_at)
        self.db.add(token)
        self.db.commit()
        return {"access_token":acc_token,"refresh_token":ref_token,"expiry_at":expiry_at}
        
    async def get_by_email(self,email:str)->models.User | None:
        result =  self.db.query(models.User).filter(models.User.email == email).first()
        return result
    async def validate_by_email_id(self,email:str,id:int)->models.User | None:
        result =  self.db.query(models.User).filter(models.User.email == email).filter(models.User.id == id).first()
        return result
    
    async def get_by_id(self,id:int)->models.User | None:
        result =  self.db.query(models.User).filter(models.User.id == id).first()
        return result
    
    async def authenticate(self,email:str,password:str)->models.User | None:
        user = await self.get_by_email(email)
        if not user or not verify_password(password,user.password) or not user.status:
            raise UserNotFoundException()
        return user
    
    async def create_user(self,user:schema.UserCreate)->models.User:
        if await self.get_by_email(user.email):
            raise EmailAlreadyExists()
        hashed_password = password_hash(user.password)
        db = models.User(name=user.name,email=user.email,password=hashed_password,phone=user.phone)
        self.db.add(db)
        self.db.commit()
        self.db.refresh(db)
        return db
    

    async def get_all_users(self,page:int=1,limit:int=5)->list[models.User]:
        total = self.db.query(models.User).count()

        total_pages = ceil(total / limit) if total > 0 else 1

        if page > total_pages:
            raise DataLimitation(total_pages)

        offset = (page-1)*limit
        result = self.db.query(models.User).offset(offset).limit(limit).all()
        return {"total":total,"page":page,"limit":limit,"data":result}
    

    async def delete_user(self,id:int):
        if await self.get_by_id(id) is None:
            raise UserNotFoundException()
        self.db.query(models.User).filter(models.User.id == id).update({"deleted_at": True})
        self.db.commit()
        return True

    async def user_update(self,id:int,user:schema.UserUpdate,role:str):
        print(f"what is role ----> {role}")
        user_row = await self.get_by_id(id)
        if user_row is None:
            raise UserNotFoundException()        
        
        update_data = {
            "name": user.name if user.name is not None else user_row.name,
            "phone": user.phone if user.phone is not None else user_row.phone,
        }
        if role == "admin":
            if user.status is not None:
                update_data["status"] = user.status

            if user.role is not None:
                update_data["role"] = user.role

        self.db.query(models.User).filter(models.User.id == id).update(update_data)

        self.db.commit()
        return True
    
class TokenManagementService:
    def __init__(self,db:Session):
        self.db = db

    async def refresh_token_verify(self,refresh_token:str)->models.TokenManagement | None:
        result = self.db.query(models.TokenManagement).filter(models.TokenManagement.refresh_token == refresh_token).first()
        if result is None or result.revoked or result.expires_at < datetime.now(timezone.utc):
            raise InvalidToken()
        return True