from enum import Enum, auto


class UpdateState(Enum):
    UNKNOWN = auto()
    SEARCHING = auto()
    OUTDATED = auto()
    UPDATED = auto()
