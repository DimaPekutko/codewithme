from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from db import Base
from db.models import *


class SignInRecord(Base):
    __tablename__ = "sign_in_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sign_in_records")
    signed_in_at = Column(DateTime, server_default=func.now())
