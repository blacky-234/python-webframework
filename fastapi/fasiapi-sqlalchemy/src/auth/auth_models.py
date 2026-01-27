from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from database import Base


class TokenManagement(Base):

    __tablename__ = "tokens"

    id()