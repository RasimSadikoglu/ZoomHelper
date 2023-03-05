from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID, uuid4
from helper.helper import zh_find, zh_for_each

from models.time.base_time import BaseTime
from models.meeting.meeting_status import MeetingStatus


class BaseMeeting(ABC):
    __name: str
    __guid: UUID
    __calendar: list[BaseTime]

    def __init__(self, name: str) -> None:
        self.__name = name

        self.__guid = uuid4()
        self.__calendar = []

    @abstractmethod
    def open_meeting(self) -> None:
        ...

    def add_entry_to_calendar(self, *entries: BaseTime) -> None:
        self.__calendar.extend(entries)

    def check_time(self) -> MeetingStatus:
        times = [x.check_time() for x in self.__calendar]

        if zh_find(times, lambda x: x == MeetingStatus.CURRENT):
            return MeetingStatus.CURRENT

        if zh_find(times, lambda x: x != MeetingStatus.PAST):
            return MeetingStatus.PAST

        return MeetingStatus.FUTURE
