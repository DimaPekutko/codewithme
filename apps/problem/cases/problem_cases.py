from typing import List
from fastapi.exceptions import HTTPException

from db.orm import Base
from apps.users.schemas import User

from ..storages import ProblemStorage
from ..schemas import DefaultProblem, FullProblem, CodeAssertion, BaseUpdateSchema, UpdateActiveLangs, \
    ProblemCategory, UpdateCategories
from ..types import ProblemStatus
from ..services import PythonBuilder


class ProblemCases():
    def __init__(self, repo: ProblemStorage) -> None:
        self.repo = repo

    async def new_problem(self, user: User) -> FullProblem:
        problem = DefaultProblem(
            title="Default",
            desc="Default",
            complexity_level=5,
            author_id=user.id,
            status=ProblemStatus.disabled,
            categories=[]
        )
        problem_id = await self.repo.new_problem(problem)
        return await self.repo.get(problem_id)

    async def get_lang_problem(self, id: int) -> List[FullProblem]:
        return await self.repo.get_lang_problem(lproblem_id=id)

    async def get_problems(self, user: User) -> List[FullProblem]:
        return await self.repo.get_all()

    async def toggle_problem(self, problem_id: int):
        problem = await self.repo.get(problem_id)
        new_status = ProblemStatus.disabled if problem.status == ProblemStatus.active else ProblemStatus.active

        if new_status == ProblemStatus.active:
            if len(problem.categories) < 2:
                raise HTTPException(status_code=400, detail="Problem must have at least two categories")

            if not len(problem.langs):
                raise HTTPException(status_code=400, detail="Problem must have at least one language support")

            if len(problem.title) < 5:
                raise HTTPException(status_code=400, detail="Problem title must be at least 5 characters long")

            if len(problem.desc) < 20:
                raise HTTPException(status_code=400, detail="Problem description must be at least 20 characters long")

            try:
                await PythonBuilder.build_code(problem.lang_problems[0])
            except ValueError as err:
                raise HTTPException(status_code=400, detail=f'Can not parse problem code, {str(err)}')

        await self.repo.update_problem_status(problem_id, new_status)

        problem.status = new_status
        return problem

    async def partial_update(self, model: Base, target_id: int, payload: BaseUpdateSchema) -> BaseUpdateSchema:
        await self.repo.update(model, target_id, payload)
        return payload

    async def add_assertion(self, lang_problem_id: int) -> CodeAssertion:
        return await self.repo.add_assertion(lang_problem_id)

    async def update_categories(self, problem_id: int, payload: UpdateCategories) -> UpdateCategories:
        return await self.repo.update_categories(problem_id, payload)

    async def update_active_langs(self, problem_id: int, payload: UpdateActiveLangs) -> UpdateActiveLangs:
        await self.repo.update_active_langs(problem_id, payload)
        return payload

    async def get_all_categories(self) -> List[ProblemCategory]:
        return await self.repo.get_all_categories()

    async def delete_assertion(self, assertion_id: int):
        await self.repo.delete_assertion(assertion_id)

    async def delete_problem(self, problem_id: int):
        await self.repo.delete_problem(problem_id)
