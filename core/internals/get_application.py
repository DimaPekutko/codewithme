from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from fastapi_socketio import SocketManager
from .get_routers import GetRouters
from .decorate_fast_api import decorate_fast_api
from ..loggers.log_request import log_requets_params
from settings import LOG_REQUEST


SUPPORTED_VERSIONS = ("v1",)


def get_application() -> FastAPI:
    """
    Makes Fast API instance,
    Add middlewares,
    Import all routers and are in router_<x>.py files
    """
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3069"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    SocketManager(app=app, mount_location="/ws", socketio_path="/", cors_allowed_origins=[])

    for version in SUPPORTED_VERSIONS:
        routers_data = GetRouters.call(version)

        for router_data in routers_data:
            if router_data.get("prefix"):
                prefix = f"/api/{version}/{router_data.get('prefix')}"
            else:
                prefix = f"/api/{version}"

            extra_params = router_data.get("extra_params", {})

            if LOG_REQUEST:
                # Based on settings logging request with body and headers
                dependencies = extra_params.pop("dependencies", [])
                dependencies.append(Depends(log_requets_params))

            app.include_router(router_data["router"], prefix=prefix, **extra_params, dependencies=dependencies)

    # decorate Fast API application with some additional handlers for events, requests, etc
    decorate_fast_api(app)

    return app


fast_api = get_application()
