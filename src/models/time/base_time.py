from abc import ABC, abstractmethod

from models.meeting.meeting_status import MeetingStatus


class BaseTime(ABC):
    @abstractmethod
    def check_time(self) -> MeetingStatus:
        ...
