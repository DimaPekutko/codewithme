from ..schemas import SignIn, SignUp, GoogleSignIn, AuthResponse, RefreshTokenSchema, AccessTokenSchema
from ..storages import SignInStorage
from ....schemas.user_create import UserCreate

from apps.users.schemas import AuthUser
from apps.users.storages import UsersStorage
from apps.users import types
from apps.users.storages.users_storage import validate_password
from core import AuthToken, AppException


class AuthCases:
    def __init__(self, users_repo: UsersStorage, sign_in_repo: SignInStorage):
        self._users_repo = users_repo
        self._sign_in_repo = sign_in_repo

    async def google_sign_in(self, data: GoogleSignIn) -> AuthResponse:
        user = await self._users_repo.get_user_by_identity(data.email)

        if not user:
            return await self.sign_up(
                SignUp(
                    email=data.email,
                    full_name=data.name,
                    picture=data.picture,
                    password="google_way",
                ),
                avoid_check=True,
            )

        tokens_pair = AuthToken.generate_pair(user.dict())
        return AuthResponse(user=user, **tokens_pair)

    async def sign_in(self, data: SignIn) -> AuthResponse:
        user = await self._users_repo.get_user_by_identity(data.email)

        if not user or user.register_strategy != types.RegisterStrategy.default:
            raise AppException("auth.email_password_invalid")

        if not validate_password(data.password, user.hashed_password):
            raise AppException("auth.email_password_invalid")

        tokens_pair = AuthToken.generate_pair(user.dict())
        await self._track_sign_in(user)
        return AuthResponse(user=user, **tokens_pair)

    async def _track_sign_in(self, user: AuthUser) -> None:
        await self._sign_in_repo.create(user)

    async def sign_up(self, data: SignUp, avoid_check: bool = False) -> AuthResponse:
        if not avoid_check:
            user = await self._users_repo.get_user_by_identity(data.email)

            if user:
                raise AppException("sign_up.user_exists")

        user = await self._users_repo.create_user(UserCreate(**data.dict()))
        tokens_pair = AuthToken.generate_pair(user.dict())
        return AuthResponse(user=user, **tokens_pair)

    async def refresh_token(self, data: RefreshTokenSchema) -> AccessTokenSchema:
        data = AuthToken.decrypt_token(data.refresh_token)
        return AccessTokenSchema(access_token=AuthToken.generate_access_token(data))
