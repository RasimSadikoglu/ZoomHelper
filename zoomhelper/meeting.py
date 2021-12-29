from os import system
from sys import platform
from datetime import datetime

class Meeting:

    def __init__(self, name: str, id: str, password: str, date: dict, weekDay: int, time: str, isFree: bool):
        self.name = name
        self.id = id
        self.password = password
        self.date = datetime(**date) if date != None else None
        self.weekDay = weekDay
        self.isFree = isFree
        self.time = time

    def open(self) -> None:
        if platform == "win32":
            url = f'%APPDATA%/Zoom/bin/Zoom.exe "-url=zoommtg://zoom.us/join?action=join&confno={self.id}&pwd={self.password}"'
        elif platform == "darwin":
            url = f'open /Applications/zoom.us.app "--url=zoommtg://zoom.us/join?action=join&confno={self.id}&pwd={self.password}"'

        system(url)

    def check(self, startTimeOffset, endTimeOffset) -> bool:
        now = datetime.now()

        if self.isFree:
            return True
        
        if self.weekDay != None and self.weekDay != now.weekday():
            return False

        if self.date != None and self.date != now.date():
            return False

        startTime, endTime = self.time.split('-')
        startTime, endTime = startTime.split('.'), endTime.split('.')

        startTime = int(startTime[0]) * 60 + int(startTime[1]) + startTimeOffset
        endTime = int(endTime[0]) * 60 + int(endTime[1]) + endTimeOffset

        now = now.hour * 60 + now.minute

        return now >= startTime and now <= endTime

    def jsonSerialize(self) -> dict:
        return self.__dict__

    def jsonDeserialize(meeting) -> object:
        return Meeting(**meeting)