from datetime import datetime

from ..models import SignInRecord

from apps.users.schemas import AuthUser
from db import async_session


class SignInStorage:
    _table = SignInRecord

    @classmethod
    async def create(cls, user: AuthUser) -> None:
        async with async_session() as session:
            sign_in_record = cls._table(user_id=user.id, signed_in_at=datetime.now())
            session.add(sign_in_record)
            await session.commit()
