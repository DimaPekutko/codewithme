import sqlalchemy as sa
from sqlalchemy.orm import joinedload
from typing import List
from pydantic import TypeAdapter

from db.orm import Base
from db import async_session
from .. import models, types, schemas, lang_templates


class ProblemStorage:
    async def get_lang_problem(self, lproblem_id: int) -> schemas.FullLangProblem:
        async with async_session() as session:
            q = sa.select(models.LangProblem).where(models.LangProblem.id == lproblem_id)
            q = q.options(
                joinedload(models.LangProblem.problem).joinedload(models.Problem.categories),
                joinedload(models.LangProblem.assertions),
            )

            cursor = await session.execute(q)
            problem: models.Problem = cursor.unique().scalar_one()

            return schemas.FullLangProblem.model_validate(problem)

    async def get(self, problem_id: int) -> schemas.FullProblem:
        async with async_session() as session:
            q = sa.select(models.Problem).where(models.Problem.id == problem_id)
            q = q.options(
                joinedload(models.Problem.lang_problems).joinedload(models.LangProblem.assertions),
                joinedload(models.Problem.categories),
            )

            cursor = await session.execute(q)
            problem: models.Problem = cursor.unique().scalar_one()

            return schemas.FullProblem.model_validate(problem)

    async def get_all(self) -> List[schemas.FullProblem]:
        async with async_session() as session:
            q = sa.select(models.Problem).order_by(models.Problem.created_at)

            joins = [
                joinedload(models.Problem.lang_problems).joinedload(models.LangProblem.assertions),
                joinedload(models.Problem.categories),
            ]

            q = q.options(*joins)

            cursor = await session.execute(q)
            problems: List[models.Problem] = cursor.unique().scalars().all()

            return TypeAdapter(List[schemas.FullProblem]).validate_python(problems)

    async def new_problem(self, problem: schemas.DefaultProblem) -> int:
        async with async_session() as session:
            # create problem
            problem = models.Problem(**problem.model_dump())
            session.add(problem)
            # create lang problems and internal code asserions
            problem.lang_problems = [
                models.LangProblem(
                    language=types.Language.python,
                    code_context=lang_templates.python.DEFAULT_CONTEXT,
                    initial_code=lang_templates.python.DEFAULT_INIT,
                    status=types.ProblemLangStatus.active,
                    assertions=[models.CodeAssertion(code=lang_templates.python.DEFAULT_ASSERT)],
                ),
            ]
            await session.commit()
            return problem.id

    async def update_problem_status(self, problem_id: int, status: types.ProblemStatus):
        async with async_session() as session:
            q = sa.update(models.Problem).where(models.Problem.id == problem_id).values(status=status)
            await session.execute(q)
            await session.commit()

    async def update(self, model: Base, target_id: int, payload: schemas.BaseUpdateSchema):
        async with async_session() as session:
            q = sa.update(model).where(model.id == target_id).values(payload.model_dump(exclude_unset=True))
            await session.execute(q)
            await session.commit()

    async def update_categories(
        self, problem_id: int, payload: schemas.UpdateCategories
    ) -> List[schemas.ProblemCategory]:
        async with async_session() as session:
            q = sa.select(models.Problem).where(models.Problem.id == problem_id)

            cursor = await session.execute(q)
            problem: models.Problem = cursor.unique().scalar_one()

            q = sa.select(models.ProblemCategory).where(models.ProblemCategory.name.in_(payload.categories))
            cursor = await session.execute(q)
            categories: List[models.ProblemCategory] = cursor.scalars().all()

            problem.categories = categories
            await session.commit()
            return TypeAdapter(List[schemas.ProblemCategory]).validate_python(categories)

    async def update_active_langs(self, problem_id: int, payload: schemas.UpdateActiveLangs):
        async with async_session() as session:
            active = types.ProblemLangStatus.active.value
            disabled = types.ProblemLangStatus.disabled.value

            q = (
                sa.update(models.LangProblem)
                .where(models.LangProblem.problem_id == problem_id)
                .values(
                    status=sa.case([(models.LangProblem.language.in_(payload.langs), active)], else_=disabled).cast(
                        sa.Enum(types.ProblemLangStatus)
                    )
                )
            )

            await session.execute(q)
            await session.commit()

    async def add_assertion(self, lang_problem_id: int) -> schemas.CodeAssertion:
        async with async_session() as session:
            code = "test assertion"

            assertion = models.CodeAssertion(lang_problem_id=lang_problem_id, code=code)
            session.add(assertion)

            await session.commit()
            return schemas.CodeAssertion(id=assertion.id, code=code)

    async def delete_assertion(self, assertion_id: int):
        async with async_session() as session:
            q = sa.delete(models.CodeAssertion).where(models.CodeAssertion.id == assertion_id)
            await session.execute(q)
            await session.commit()

    async def delete_problem(self, problem_id: int):
        async with async_session() as session:
            q = sa.delete(models.Problem).where(models.Problem.id == problem_id)
            await session.execute(q)
            await session.commit()

    async def get_all_categories(self) -> List[schemas.ProblemCategory]:
        async with async_session() as session:
            q = sa.select(models.ProblemCategory)

            cursor = await session.execute(q)
            categories: List[models.ProblemCategory] = cursor.scalars().all()

            return TypeAdapter(List[schemas.ProblemCategory]).validate_python(categories)
