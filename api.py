import uvicorn
import settings
from core import logger
from core.internals.get_application import fast_api # noqa # pylint: disable=unused-import
from apps.playground.socket_router import *


# use 'api:fast_api' to run using uvicorn/gunicorn like the folliwing:
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:fast_api
# instead of using uvicorn/gunicorn directly in python like below


if __name__ == "__main__":
    logger.info(f"Application is working on {settings.PORT} port\n")
    uvicorn.run("api:fast_api", host=settings.HOST, port=settings.PORT,
                log_level=settings.LOG_LEVEL.lower(), reload=settings.HOT_RELOAD)
