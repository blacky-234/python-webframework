from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from Database import Base
from datetime import datetime



class User(Base):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String,nullable=False)
    phone = Column(String(15),nullable=True)
    role = Column(String(50),default="user")
    status = Column(Boolean, default=True)
    deleted_at = Column(Boolean, default=False)
    refresh_tokens = relationship("TokenManagement",back_populates="user",cascade="all, delete-orphan")


class TokenManagement(Base):

    __tablename__ = "tokens"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    refresh_token = Column(String(255),nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    user = relationship("User", back_populates="refresh_tokens") 
