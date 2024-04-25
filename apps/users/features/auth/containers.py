from dependency_injector import containers, providers

from .cases import AuthCases
from .storages import SignInStorage
from ...storages import UsersStorage


class Container(containers.DeclarativeContainer):
    user_storage = providers.Singleton(
        UsersStorage,
    )

    sign_in_storage = providers.Singleton(
        SignInStorage,
    )

    auth_cases = providers.Singleton(
        AuthCases,
        users_repo=user_storage,
        sign_in_repo=sign_in_storage,
    )
