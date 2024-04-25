import hashlib
import random
import string
import sqlalchemy as sa
from typing import List
from pydantic import TypeAdapter

from passlib.context import CryptContext
from sqlalchemy.future import select

from ..schemas import User, UserCreate, AuthUser
from ..models.user import User as UserModel

from db import async_session


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersStorage:
    _table = UserModel
    """
    This class is responsible for CRUDL operations for User entity
    and responsible only for CRUDL with minimal validations and mostly
    with queries to DB
    """

    @classmethod
    async def create_user(cls, user: UserCreate) -> User:
        salt = get_random_string()
        hashed_password = hash_password(user.password, salt)

        async with async_session() as session:
            user = cls._table(
                email=user.email,
                full_name=user.full_name,
                picture=str(user.picture),
                hashed_password=f"{salt}${hashed_password}",
            )
            session.add(user)
            await session.commit()
        return await cls.get_user(user.id)

    @classmethod
    async def get_user_by_identity(cls, email: str) -> AuthUser:
        async with async_session() as session:
            query = await session.execute(select(cls._table).filter(cls._table.email == email and email.lower()))
            user = query.scalars().first()
        result = user and AuthUser.model_validate(user)
        return result

    @classmethod
    async def get_users(cls) -> List[User]:
        async with async_session() as session:
            query = await session.execute(select(cls._table))
            users = query.scalars().all()
        return TypeAdapter(List[User]).validate_python(users)

    @classmethod
    async def get_user(cls, user_id: int) -> User:
        async with async_session() as session:
            query = await session.execute(select(cls._table).where(cls._table.id == user_id))
            user = query.scalars().first()
            return User.model_validate(user)

    @classmethod
    async def set_user_status(cls, user_id: int, to_block: bool = False) -> List[User]:
        async with async_session() as session:
            q = sa.update(cls._table).where(cls._table.id == user_id).values(is_blocked=to_block)
            await session.execute(q)
            await session.commit()
