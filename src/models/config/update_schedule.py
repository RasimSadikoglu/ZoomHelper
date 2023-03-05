from enum import Enum, auto


class UpdateSchedule(Enum):
    MANUEL = auto()
    DAILY = auto()
    ALWAYS = auto()
