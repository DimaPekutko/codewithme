import docker
from datetime import datetime

from core.internals import celery_app, celery
from apps.problem.services import PythonBuilder
from apps.problem.storages import ProblemStorage
from .. import schemas, storages, types


PYTHON_DOCKER_IMG = "pythonlang_docker"


class ExecutionService:
    def __init__(self) -> None:
        self.problem_storage = ProblemStorage()
        self.playground_storage = storages.PlaygroundStorage()

    async def _run_in_container(self, code: str) -> schemas.ExecutionResult:
        client = docker.APIClient()

        container = client.create_container(PYTHON_DOCKER_IMG, stdin_open=True)
        sock = client.attach_socket(container, params={"stdin": 1, "stdout": 1, "stderr": 1, "stream": 1})

        # start
        client.start(container)
        sock._sock.send(bytes(code, encoding="utf-8"))
        sock._sock.close()
        sock.close()

        # wait for status code
        status = client.wait(container)

        status_code = status["StatusCode"]
        stdout = client.logs(container, stderr=False).decode()
        stderr = client.logs(container, stdout=False).decode()

        if stderr or status_code != 0:
            raise ValueError(stderr)

        # remove created container
        client.remove_container(container)

        return schemas.ExecutionResult.model_validate_json(stdout)

    async def _run(self, runtime: schemas.Runtime):
        lproblem = await self.problem_storage.get_lang_problem(runtime.lang_problem_id)
        lproblem.initial_code = runtime.code

        try:
            whole_code = await PythonBuilder.build_code(lproblem)

            result = await self._run_in_container(code=whole_code)
            new_status = types.RuntimeStatus.failed if result.failed else types.RuntimeStatus.completed

            output = result.errors[0] if len(result.errors) else "all tests are passed"

        except ValueError as err:
            result = schemas.ExecutionResult(passed=0, failed=0, errors=[str(err)])
            new_status = types.RuntimeStatus.failed
            output = str(err)

        # update runtime
        update_payload = schemas.RuntimeUpdatePayload(
            tests_passed=result.passed,
            tests_failed=result.failed,
            finish_date=datetime.utcnow(),
            status=new_status,
            output=output,
        )
        await self.playground_storage.update_runtime(runtime.id, update_payload)

        # update game if need
        if runtime.game_id and new_status == types.RuntimeStatus.completed:
            game_payload = schemas.FinishGamePayload(winner_id=runtime.user_id, status=types.GameStatus.finished)
            await self.playground_storage.finish_game(runtime.game_id, game_payload)

    @staticmethod
    @celery_app.task(name="coderun_task")
    def run_code(runtime: dict):
        es = ExecutionService()
        runtime = schemas.Runtime(**runtime)

        celery.event_loop.run_until_complete(es._run(runtime))
