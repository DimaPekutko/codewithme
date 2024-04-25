from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from typing import Optional

from .containers import Container
from core.auth import get_user, AuthRoute
from apps.users.schemas import User
from . import schemas, services
from .storages import PlaygroundStorage


router = APIRouter(route_class=AuthRoute)


@router.post("/playground/{lproblem_id}/submit")
@inject
async def submit(
    payload: schemas.SubmitPayload,
    lproblem_id: int,
    user: User = Depends(get_user),
    storage: PlaygroundStorage = Depends(Provide[Container.playground_storage]),
):
    runtime_payload = schemas.RuntimePayload(
        user_id=user.id, lang_problem_id=lproblem_id, code=payload.code, game_id=payload.game_id
    )

    runtime = await storage.create_runtime(runtime_payload)
    services.ExecutionService.run_code.delay(runtime.model_dump())

    return runtime


@router.get("/playground/{lproblem_id}/runtimes")
@inject
async def runtimes(
    lproblem_id: int,
    user_id: Optional[int] = None,
    game_id: Optional[int] = None,
    user: User = Depends(get_user),
    storage: PlaygroundStorage = Depends(Provide[Container.playground_storage]),
):
    return await storage.get_runtimes(lproblem_id, user_id or user.id, game_id)


@router.get("/runtimes/{runtime_id}/")
@inject
async def runtime(
    runtime_id: int,
    user: User = Depends(get_user),
    storage: PlaygroundStorage = Depends(Provide[Container.playground_storage]),
):
    return await storage.get_runtime(runtime_id)


@router.get("/games/{game_id}/")
@inject
async def game(
    game_id: int,
    user: User = Depends(get_user),
    storage: PlaygroundStorage = Depends(Provide[Container.playground_storage]),
):
    return await storage.get_game(game_id)


@router.get("/games")
@inject
async def games(
    user_id: int,
    user: User = Depends(get_user),
    storage: PlaygroundStorage = Depends(Provide[Container.playground_storage]),
):
    return await storage.get_games(user_id=user_id)


container = Container()
container.wire(modules=[__name__])
