import socketio
import json
from socketio.exceptions import ConnectionRefusedError
import uuid

from core.internals.get_application import fast_api
from core.auth.auth_token import AuthToken
from apps.users.schemas.user import AuthUser

from . import schemas, storages, types


sio: socketio.AsyncServer = fast_api.sio

storage = storages.PlaygroundStorage()


async def get_user(sid: str) -> AuthUser:
    return (await sio.get_session(sid))["user"]


async def gen_room_id() -> str:
    return uuid.uuid4().hex[:24]


@sio.event
async def connect(sid: str, environ, auth):
    token = auth.get("token", " ").split(" ")[-1]
    try:
        await sio.save_session(sid, {"user": AuthUser(**AuthToken.decrypt_token(token))})
    except Exception:
        raise ConnectionRefusedError("Auth failed")


@sio.on("search_problem")
async def search_problem(sid: str, data: dict, *args, **kwargs):
    payload = schemas.SearchGamePayload(**data)

    # execute start of offline game immediately
    if payload.game_type == "offline":
        lproblem_id = await storage.find_problem_by_params(payload)
        await sio.emit("game_started", {"lproblem_id": lproblem_id})
        return

    # TODO: make this O(log n) or O(1) instead of O(n) and remove json
    for room, clients in sio.manager.rooms["/"].copy().items():
        # find room with json struccture as name
        try:
            room_payload = schemas.SearchGamePayload.model_validate_json(room)
        except Exception:
            continue
        # find payloads intersection
        try:
            common_payload = payload & room_payload
        except ValueError:
            continue

        # create new game room
        game_room = await gen_room_id()

        opponents = list(clients.keys())
        if not len(opponents):
            continue
        opponent_sid = opponents[0]

        # assigning clients to room
        await sio.enter_room(sid, game_room)
        await sio.enter_room(opponent_sid, game_room)

        # create game in db
        user = await get_user(sid)
        opponent = await get_user(opponent_sid)

        if user.id == opponent.id:
            continue

        # create game
        lproblem_id = await storage.find_problem_by_params(common_payload)
        game_id = await storage.create_game(lproblem_id, opponent.id, user.id, game_room)

        # notify room
        await sio.emit("game_started", {"game_id": game_id}, room=game_room)
        # close lobby's room
        await sio.close_room(room)
        return

    await sio.enter_room(sid, json.dumps(data))


@sio.on("stop_search_problem")
async def stop_search_problem(sid: str, data: dict, *args, **kwargs):
    rooms = sio.rooms(sid)
    [await sio.leave_room(sid, room) for room in rooms]


@sio.on("join_game")
async def join_game(sid: str, data: dict, *args, **kwargs):
    game_id = int(data.get("game_id", ""))
    game = await storage.get_game(game_id)

    await sio.enter_room(sid, game.room_uid)


@sio.on("client_runtime_finished")
async def runtime_finished(sid: str, data: dict, *args, **kwargs):
    runtime_id = data.get("runtime_id", 0)

    runtime = await storage.get_runtime(runtime_id)
    game = await storage.get_game(runtime.game_id)

    await sio.emit(
        "game_runtime_finished",
        {"user_id": runtime.user_id, "failed": runtime.tests_failed, "passed": runtime.tests_passed},
        room=game.room_uid,
    )

    if game.status == types.GameStatus.finished:
        await sio.emit("game_finished", game.model_dump(), room=game.room_uid)


@sio.event
async def disconnect(sid: str):
    rooms = sio.rooms(sid)
    [await sio.leave_room(sid, room) for room in rooms]
