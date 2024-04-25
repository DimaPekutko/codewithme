from dependency_injector import containers, providers

from .storages import UsersStorage


class Container(containers.DeclarativeContainer):
    user_storage = providers.Singleton(UsersStorage)
