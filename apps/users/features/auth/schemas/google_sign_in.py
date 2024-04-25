from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class GoogleSignIn(BaseModel):
    email: EmailStr
    email_verified: bool
    name: str
    picture: Optional[HttpUrl] = None
