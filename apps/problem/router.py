from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from .cases import ProblemCases
from .containers import Container
from core.auth import get_user, AuthRoute
from apps.users.schemas import User
from .schemas import (
    FullProblem,
    ProblemForUpdate,
    LangProblemForUpdate,
    CodeAssertionForUpdate,
    UpdateActiveLangs,
    UpdateCategories,
)
from . import models


router = APIRouter(route_class=AuthRoute)


@router.post("/problems/new")
@inject
async def new_problem(
    user: User = Depends(get_user), problem_cases: ProblemCases = Depends(Provide[Container.problem_cases])
) -> FullProblem:
    return await problem_cases.new_problem(user)


@router.get("/problems")
@inject
async def problems(
    user: User = Depends(get_user), problem_cases: ProblemCases = Depends(Provide[Container.problem_cases])
):
    return await problem_cases.get_problems(user)


@router.get("/lang_problems/{lproblem_id}")
@inject
async def lang_problem(
    lproblem_id: int,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    return await problem_cases.get_lang_problem(lproblem_id)


@router.post("/problems/{problem_id}/toggle")
@inject
async def toggle(
    problem_id: int,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    return await problem_cases.toggle_problem(problem_id)


@router.get("/categories")
@inject
async def categories(
    user: User = Depends(get_user), problem_cases: ProblemCases = Depends(Provide[Container.problem_cases])
):
    return await problem_cases.get_all_categories()


@router.patch("/problems/{problem_id}")
@inject
async def update_problem(
    problem_id: int,
    payload: ProblemForUpdate,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    return await problem_cases.partial_update(models.Problem, problem_id, payload)


@router.patch("/problems/{problem_id}/categories")
@inject
async def update_categories(
    problem_id: int,
    payload: UpdateCategories,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    return await problem_cases.update_categories(problem_id, payload)


@router.patch("/problems/{problem_id}/active_langs")
@inject
async def update_active_langs(
    problem_id: int,
    payload: UpdateActiveLangs,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    return await problem_cases.update_active_langs(problem_id, payload)


@router.patch("/lang_problems/{lproblem_id}")
@inject
async def update_lang_problem(
    lproblem_id: int,
    payload: LangProblemForUpdate,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    return await problem_cases.partial_update(models.LangProblem, lproblem_id, payload)


@router.patch("/code_assertions/{assertion_id}")
@inject
async def update_assertion(
    assertion_id: int,
    payload: CodeAssertionForUpdate,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    return await problem_cases.partial_update(models.CodeAssertion, assertion_id, payload)


@router.delete("/code_assertions/{assertion_id}")
@inject
async def delete_assertion(
    assertion_id: int,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    await problem_cases.delete_assertion(assertion_id)
    return {}


@router.post("/lang_problems/{lang_problem_id}/add_test")
@inject
async def add_assertion(
    lang_problem_id: int,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    return await problem_cases.add_assertion(lang_problem_id)


@router.delete("/problems/{problem_id}")
@inject
async def delete_problem(
    problem_id: int,
    user: User = Depends(get_user),
    problem_cases: ProblemCases = Depends(Provide[Container.problem_cases]),
):
    await problem_cases.delete_problem(problem_id)
    return {}


container = Container()
container.wire(modules=[__name__])
