import sqlalchemy as sa
from sqlalchemy.orm import joinedload
from typing import List, Optional
from pydantic import TypeAdapter

from db import async_session
from apps.problem import models as problem_models, types as problem_types
from .. import schemas, models, types


class PlaygroundStorage():

    async def get_runtime(self, runtime_id: int) -> schemas.FullRuntime:
        async with async_session() as session:
            q = sa.select(models.Runtime).where(models.Runtime.id == runtime_id)

            cursor = await session.execute(q)
            runtime: models.Runtime = cursor.unique().scalar_one()

            return schemas.FullRuntime.model_validate(runtime)

    async def get_runtimes(self, lproblem_id: int, user_id: int, game_id: Optional[int]) -> List[schemas.FullRuntime]:
        async with async_session() as session:
            q = sa.select(models.Runtime).where(models.Runtime.lang_problem_id == lproblem_id,
                                                models.Runtime.user_id == user_id)
            if game_id:
                q = q.where(models.Runtime.game_id == game_id)

            q = q.order_by(models.Runtime.finish_date.desc())

            cursor = await session.execute(q)
            runtimes: List[models.Runtime] = cursor.scalars().all()

            return TypeAdapter(List[schemas.FullRuntime]).validate_python(runtimes)

    async def create_runtime(self, payload: schemas.RuntimePayload) -> schemas.Runtime:
        async with async_session() as session:
            runtime = models.Runtime(**payload.model_dump())
            session.add(runtime)
            await session.commit()
            return schemas.Runtime(id=runtime.id, status=runtime.status, **payload.model_dump())

    async def update_runtime(self, runtime_id: int, payload: schemas.RuntimeUpdatePayload):
        async with async_session() as session:
            q = sa.update(models.Runtime).where(models.Runtime.id == runtime_id)\
                .values(**payload.model_dump())
            await session.execute(q)
            await session.commit()

    async def get_game(self, game_id: int) -> schemas.FullGame:
        async with async_session() as session:
            q = sa.select(models.Game).where(models.Game.id == game_id)

            q = q.options(joinedload(models.Game.user1), joinedload(models.Game.user2))

            cursor = await session.execute(q)
            game: models.Game = cursor.unique().scalar_one()

            return schemas.FullGame.model_validate(game)

    async def get_games(self, user_id: int) -> schemas.FullGame:
        async with async_session() as session:
            q = sa.select(models.Game).where(sa.or_(models.Game.user1_id == user_id,
                                                    models.Game.user2_id == user_id))

            q = q.options(joinedload(models.Game.user1), joinedload(models.Game.user2))

            cursor = await session.execute(q)
            games: List[models.Game] = cursor.unique().scalars().all()

            return TypeAdapter(List[schemas.FullGame]).validate_python(games)

    async def create_game(self, lproblem_id: int, user1_id: int, user2_id: int, room_id: str) -> int:
        async with async_session() as session:
            game = models.Game(
                lang_problem_id=lproblem_id,
                user1_id=user1_id,
                user2_id=user2_id,
                room_uid=room_id
            )
            session.add(game)
            await session.commit()
            return game.id

    async def find_problem_by_params(self, payload: schemas.SearchGamePayload) -> int:
        async with async_session() as session:
            model = problem_models.LangProblem

            q = sa.select(model.id)\
                .where(model.status == problem_types.ProblemLangStatus.active,
                       problem_models.Problem.status == problem_types.ProblemStatus.active,
                       model.language.in_(payload.languages),
                       problem_models.ProblemCategory.name.in_(payload.categories),
                       problem_models.Problem.complexity_level == payload.complexity_level)

            q = q.join(problem_models.Problem,
                       problem_models.Problem.id == model.problem_id)

            q = q.join(problem_models.ProblemCatM2M,
                       problem_models.Problem.id == problem_models.ProblemCatM2M.problem_id)

            q = q.join(problem_models.ProblemCategory,
                       problem_models.ProblemCatM2M.category_id == problem_models.ProblemCategory.id)

            q = q.order_by(sa.func.random()).limit(1)

            cursor = await session.execute(q)
            lproblem_id = cursor.unique().scalar_one()

            return lproblem_id

    async def finish_game(self, game_id: int, payload: schemas.RuntimeUpdatePayload):
        async with async_session() as session:
            q = sa.update(models.Game).where(models.Game.id == game_id, models.Game.status == types.GameStatus.active)\
                .values(**payload.model_dump())
            await session.execute(q)
            await session.commit()
