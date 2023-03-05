from enum import Enum, auto


class MeetingStatus(Enum):
    PAST = auto()
    CURRENT = auto()
    FUTURE = auto()
