from datetime import datetime, timedelta
from base.config import Config
from helper.helper import get_current_datetime
from models.meeting.meeting_status import MeetingStatus
from models.time.base_time import BaseTime


class SingleTime(BaseTime):
    __start_time: datetime
    __end_time: datetime

    def __init__(self, start_time: datetime, end_time: datetime) -> None:
        self.__start_time = start_time
        self.__end_time = end_time

    @property
    def __offsetted_start_time(self) -> datetime:
        return self.__start_time + timedelta(minutes=Config().config.start_time_offset)

    @property
    def __offsetted_end_time(self) -> datetime:
        return self.__end_time + timedelta(minutes=Config().config.end_time_offset)

    def check_time(self) -> MeetingStatus:
        now = get_current_datetime()

        if now > self.__offsetted_end_time:
            return MeetingStatus.PAST

        if now < self.__offsetted_start_time:
            return MeetingStatus.FUTURE

        return MeetingStatus.CURRENT
