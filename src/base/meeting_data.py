from copy import deepcopy
from helper.helper import singleton
from models.meeting.base_meeting import BaseMeeting


@singleton
class MeetingData:
    __meetings: list[BaseMeeting]

    def __init__(self) -> None:
        self.__load()

    def __load(self) -> None:
        ...

    def __save(self) -> None:
        ...

    @property
    def meetings(self) -> list[BaseMeeting]:
        return deepcopy(self.__meetings)
