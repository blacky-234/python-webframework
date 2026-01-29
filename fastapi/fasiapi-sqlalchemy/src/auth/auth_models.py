from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class TokenManagement(Base):

    __tablename__ = "tokens"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    refresh_token = Column(String(255),nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    user = relationship("User", back_populates="refresh_tokens")