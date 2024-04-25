from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

from .. import types


class AuthUser(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    hashed_password: str
    register_strategy: types.RegisterStrategy
    picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    picture: Optional[str] = None

    winned: int = 12
    loosed: int = 32
    draws: int = 2

    rating: float
    is_blocked: bool

    model_config = ConfigDict(from_attributes=True)
