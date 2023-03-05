from datetime import datetime, timedelta
from base.config import Config
from helper.helper import get_current_datetime, get_current_time
from models.meeting.meeting_status import MeetingStatus
from models.time.base_time import BaseTime
from models.time.weekday import WeekDay


class WeeklyRepeat(BaseTime):
    __weekday: WeekDay
    __start_time: datetime
    __end_time: datetime

    def __init__(self, weekday: WeekDay, start_time: datetime, end_time: datetime) -> None:
        self.__weekday = weekday
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

        if now.weekday != self.__weekday:
            return MeetingStatus.FUTURE

        now = get_current_time()

        if not (self.__offsetted_start_time <= now <= self.__offsetted_end_time):
            return MeetingStatus.FUTURE

        return MeetingStatus.CURRENT
