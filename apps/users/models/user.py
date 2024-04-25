from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime, Enum
from sqlalchemy.sql import func, expression

from db import Base

from .. import types

from apps.playground.models import *
from apps.problem.models import *
from apps.users.models import *
from db.models import *


class User(Base):
    __tablename__ = "users"
    ADMIN = "admin"
    USER = "user"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String)
    username = Column(String)
    hashed_password = Column(String)
    register_strategy = Column(Enum(types.RegisterStrategy), default=types.RegisterStrategy.default, nullable=False)
    picture = Column(String(2048))
    is_blocked = Column(Boolean, nullable=False, server_default=expression.false())
    rating = Column(Float, nullable=False, server_default=expression.text("500"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    role = Column(String, default=USER)
    sign_in_records = relationship("SignInRecord")

    runtimes = relationship("Runtime", back_populates="user")

    games = relationship("Game", back_populates="user1", primaryjoin="User.id==Game.user1_id or User.id==Game.user2_id")

    winned_games = relationship("Game", back_populates="winner", primaryjoin="User.id==Game.winner_id")
