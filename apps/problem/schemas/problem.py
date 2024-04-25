from pydantic import BaseModel, ConfigDict, computed_field
from typing import List, Optional

from .. import types


class OrmSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProblemCategory(OrmSchema):
    id: int
    name: str


class BaseProblem(OrmSchema):
    title: str
    desc: str
    complexity_level: int
    status: types.ProblemStatus
    categories: List[ProblemCategory]


class DefaultProblem(BaseProblem):
    author_id: int


class CodeAssertion(OrmSchema):
    id: int
    code: str


class LangProblem(OrmSchema):
    id: int
    language: types.Language
    code_context: str
    initial_code: str
    assertions: List[CodeAssertion]
    status: types.ProblemLangStatus


class FullProblem(BaseProblem):

    id: int
    author_id: int
    lang_problems: List[LangProblem]

    @computed_field
    def langs(self) -> list:
        return [lp.language for lp in self.lang_problems if lp.status == types.ProblemLangStatus.active]


class FullLangProblem(LangProblem):
    problem: BaseProblem


class BaseUpdateSchema(OrmSchema):
    pass


class ProblemForUpdate(BaseUpdateSchema):
    title: Optional[str] = None
    desc: Optional[str] = None
    complexity_level: Optional[int] = None


class LangProblemForUpdate(BaseUpdateSchema):
    code_context: Optional[str] = None
    initial_code: Optional[str] = None


class CodeAssertionForUpdate(BaseUpdateSchema):
    code: str


class UpdateActiveLangs(OrmSchema):
    langs: List[types.Language]


class UpdateCategories(OrmSchema):
    categories: List[str]
