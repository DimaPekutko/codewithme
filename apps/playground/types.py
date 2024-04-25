from enum import Enum


class RuntimeStatus(str, Enum):
    processing = "processing"
    completed = "completed"
    failed = "failed"


class GameStatus(str, Enum):
    active = "active"
    finished = "finished"


class GameType(str, Enum):
    offline = "offline"
    online = "online"
