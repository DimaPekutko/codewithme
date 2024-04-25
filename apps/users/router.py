from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from .containers import Container
from core.auth import get_user, AuthRoute
from apps.users.schemas import User
from . import storages


router = APIRouter(route_class=AuthRoute)


@router.get("/users")
@inject
async def users(user: User = Depends(get_user),
                user_storage: storages.UsersStorage = Depends(Provide[Container.user_storage])):
    return await user_storage.get_users()


@router.post("/users/{user_id}/block_user")
@inject
async def block_user(user_id: int, user: User = Depends(get_user),
                     user_storage: storages.UsersStorage = Depends(Provide[Container.user_storage])):
    return await user_storage.set_user_status(user_id, to_block=True)


@router.post("/users/{user_id}/unblock_user")
@inject
async def unblock_user(user_id: int, user: User = Depends(get_user),
                       user_storage: storages.UsersStorage = Depends(Provide[Container.user_storage])):
    return await user_storage.set_user_status(user_id, to_block=False)


@router.get("/me")
@inject
async def me(user: User = Depends(get_user),
             user_storage: storages.UsersStorage = Depends(Provide[Container.user_storage])):
    return await user_storage.get_user(user.id)


@router.get("/user_profile/{user_id}")
@inject
async def user_profile(user_id: int, user: User = Depends(get_user),
                       user_storage: storages.UsersStorage = Depends(Provide[Container.user_storage])):
    return await user_storage.get_user(user_id)


container = Container()
container.wire(modules=[__name__])
