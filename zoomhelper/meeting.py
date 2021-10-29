from os import system
import datetime

weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

class Meeting:

    def __init__(self, name="", id="", password="", startDate={}, endDate={}, weekDay=-1, isFree=True, platform="Zoom"):
        self.name = name
        self.id = id
        self.password = password
        self.startDate = datetime.datetime(**startDate)
        self.endDate = datetime.datetime(**endDate)
        self.weekDay = weekDay
        self.isFree = isFree
        self.platform = platform

        self.markForDelete = False

    def open(self):
        system(f'%APPDATA%/Zoom/bin/Zoom.exe "-url=zoommtg://zoom.us/join?action=join&confno={self.id}&pwd={self.password}"')

    def info(self):
        if not self.isFree:
            date = f'{self.startDate.day}/{self.startDate.month}/{self.startDate.year}'
            time = f'{self.startDate.hour}.{self.startDate.minute} - {self.endDate.hour}.{self.endDate.minute}'
            return f'{self.name} | {date} | {time}'
        else:
            return f'{self.name} | Free'

    def labelInfo(self):
        return f'{self.name}\n{self.startDate.hour:02}.{self.startDate.minute:02} - {self.endDate.hour:02}.{self.endDate.minute:02}'

    def jsonSerialize(self):
        sd = {
            'year': self.startDate.year,
            'month': self.startDate.month,
            'day': self.startDate.day,
            'hour': self.startDate.hour,
            'minute': self.startDate.minute
        }

        ed = {
            'year': self.endDate.year,
            'month': self.endDate.month,
            'day': self.endDate.day,
            'hour': self.endDate.hour,
            'minute': self.endDate.minute
        }

        return {
            "name": self.name,
            "id": self.id,
            "password": self.password,
            "startDate": sd,
            "endDate": ed,
            "weekDay": self.weekDay,
            "isFree": self.isFree,
            "platform": self.platform
        }

    def jsonDeserialize(meeting):
        return Meeting(name=meeting["name"],
        id=meeting["id"],
        password=meeting["password"],
        startDate=meeting['startDate'],
        endDate=meeting['endDate'],
        weekDay=meeting['weekDay'],
        isFree=meeting["isFree"],
        platform=meeting["platform"])