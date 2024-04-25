from dependency_injector import containers, providers

from .storages import ProblemStorage
from .cases import ProblemCases


class Container(containers.DeclarativeContainer):
    problem_storage = providers.Singleton(ProblemStorage)

    problem_cases = providers.Singleton(ProblemCases, problem_storage)
