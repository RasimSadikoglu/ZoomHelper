from enum import Enum, auto


class UpdateSchedule(Enum):
    MANUEL = "Manuel"
    DAILY = "Daily"
    ALWAYS = "Always"
