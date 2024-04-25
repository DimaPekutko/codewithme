from pydantic import BaseModel
from apps.users.schemas import AuthUser


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: AuthUser
