from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class SignUp(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    picture: Optional[HttpUrl] = None
