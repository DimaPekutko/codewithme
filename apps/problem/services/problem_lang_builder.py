from .. import schemas
from abc import ABC


class ProblemLangBuilder(ABC):
    @staticmethod
    async def build_code(lpropblem: schemas.LangProblem):
        raise NotImplementedError
