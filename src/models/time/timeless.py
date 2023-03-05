from models.meeting.meeting_status import MeetingStatus
from models.time.base_time import BaseTime


class Timeless(BaseTime):
    def check_time(self) -> MeetingStatus:
        # TODO: return current or future depending on the configuration

        return MeetingStatus.CURRENT
