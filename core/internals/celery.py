import json
import asyncio

from celery import Celery
from kombu.serialization import register
from fastapi.encoders import jsonable_encoder

import settings

celery_app = Celery(
    "core.internals.celery",
    config_source=settings,
    include=["apps.playground.services"],
)

celery_app.conf.accept_content = [
    "application/json",
]


def jsonable_dumps(obj):
    return json.dumps(jsonable_encoder(obj))


register("jsonable", jsonable_dumps, json.loads, content_type="application/json", content_encoding="utf-8")


event_loop = asyncio.get_event_loop()
