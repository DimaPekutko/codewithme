from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from .. import types
from apps.problem import types as lang_types
from apps.users.schemas import User


class OrmSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SubmitPayload(BaseModel):
    code: str
    game_id: Optional[int] = None


class RuntimePayload(BaseModel):
    user_id: int
    lang_problem_id: int
    code: str
    game_id: Optional[int] = None


class RuntimeUpdatePayload(BaseModel):
    tests_passed: int
    tests_failed: int
    finish_date: datetime
    output: str
    status: types.RuntimeStatus


class Runtime(OrmSchema):
    id: int

    user_id: int
    lang_problem_id: int
    game_id: Optional[int] = None
    code: str

    status: types.RuntimeStatus


class FullRuntime(Runtime):
    tests_passed: Optional[int] = None
    tests_failed: Optional[int] = None
    output: Optional[str] = None

    finish_date: Optional[datetime] = None
    created_date: datetime = Field(alias="created_at")


class ExecutionResult(BaseModel):
    errors: List[str]
    passed: int
    failed: int


class SearchGamePayload(BaseModel):
    complexity_level: int
    categories: List[str] = Field(min_length=1)
    languages: List[lang_types.Language] = Field(min_length=1)
    game_type: types.GameType

    def __and__(self, other):
        return type(self)(
            complexity_level=min(self.complexity_level, other.complexity_level),
            categories=list(set(self.categories) & set(other.categories)),
            languages=list(set(self.languages) & set(other.languages)),
            game_type=self.game_type,
        )


class FullGame(OrmSchema):
    id: int
    user1: User
    user2: User
    winner_id: Optional[int] = None
    lang_problem_id: int
    status: types.GameStatus
    room_uid: str


class FinishGamePayload(OrmSchema):
    winner_id: int
    status: types.GameStatus
