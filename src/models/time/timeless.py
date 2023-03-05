from base.config import Config
from models.meeting.meeting_status import MeetingStatus
from models.time.base_time import BaseTime


class Timeless(BaseTime):
    def check_time(self) -> MeetingStatus:
        if not Config().config.open_free_meetings:
            return MeetingStatus.FUTURE

        return MeetingStatus.CURRENT
