from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,Float,Numeric,TIMESTAMP,func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    username = Column(String(50),unique=True,index=True,nullable=False)
    email = Column(String(255),unique=True,index=True,nullable=False)
    full_name = Column(String(100),nullable=True)
    password = Column(String,nullable=False)
    is_active = Column(Boolean(),default=True,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    deleted_at = Column(Boolean(),default=False,nullable=False)
    refresh_tokens = relationship("TokenManagement",back_populates="user",cascade="all, delete-orphan")
    employee = relationship("Employee",back_populates="user",cascade="all, delete-orphan")


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),unique=True,nullable=False)
    salary = Column(Numeric(10,2),nullable=True)
    user = relationship("User", back_populates="employee")

