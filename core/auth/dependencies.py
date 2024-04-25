from fastapi import Request, Depends, HTTPException, status
from apps.users.schemas.user import User


def get_user(request: Request) -> User:
    user = request.state.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"type": "auth.not_authorized"},
        )
    return user


def get_active_user(user: User = Depends(get_user)):
    return user


def get_admin_user(user: User = Depends(get_user)) -> User:
    return user
