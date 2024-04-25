from dependency_injector import containers, providers

from .storages import PlaygroundStorage


class Container(containers.DeclarativeContainer):
    playground_storage = providers.Singleton(PlaygroundStorage)
