from os import system, getenv
from sys import platform
from datetime import datetime
import subprocess, time, psutil
import webbrowser

class Status(enumerate):
    OLD = 0
    READY = 1
    NOTYET = 2

class Meeting:

    def __init__(self, name: str, id: str, password: str, date: dict, weekDay: int, time: str, isFree: bool):
        self.name = name
        self.id = id
        self.password = password
        self.date = datetime(**date).date() if date != None else None
        self.weekDay = weekDay
        self.isFree = isFree
        self.time = time

        self.markForDelete = False

    def update(self, name: str, id: str, password: str, date: dict, weekDay: int, time: str, isFree: bool):
        self.name = name
        self.id = id
        self.password = password
        self.date = datetime(**date).date() if date != None else None
        self.weekDay = weekDay
        self.isFree = isFree
        self.time = time

        self.markForDelete = False

    def open(self):
        if platform in ['win32', 'cygwin', 'msys']:
            zoomProcess = len(list(filter(lambda p: p.name() == 'Zoom.exe', psutil.process_iter())))

            if zoomProcess == 0:
                subprocess.Popen([getenv('APPDATA') + '/Zoom/bin/Zoom.exe'])
                time.sleep(5)

            url = f'{getenv("APPDATA") + "/Zoom/bin/Zoom.exe"} "-url=zoommtg://zoom.us/join?action=join&confno={self.id}&pwd={self.password}"'
        elif platform == 'darwin':
            url = f'open /Applications/zoom.us.app "--url=zoommtg://zoom.us/join?action=join&confno={self.id}&pwd={self.password}"'
        elif platform in ['linux', 'linux2']:
            zoomProcess = len(list(filter(lambda p: p.name() == 'zoom', psutil.process_iter())))

            if zoomProcess == 0:
                subprocess.Popen(['zoom'])
                time.sleep(5)

            url = f'xdg-open "zoommtg://zoom.us/join?action=join&confno={self.id}&pwd={self.password}"'
        else:
            url = f'https://zoom.us/j/{self.id}?pwd={self.password}'
            webbrowser.open(url)
            return
            
        system(url)

    def check(self, startTimeOffset, endTimeOffset) -> Status:
        now = datetime.now()

        if self.isFree:
            return Status.READY
        
        if self.weekDay != None and self.weekDay != now.weekday():
            return Status.NOTYET

        if self.date != None and self.date != now.date():
            return Status.OLD if self.date <= now.date() else Status.NOTYET

        startTime, endTime = self.time.split('-')
        startTime, endTime = startTime.split('.'), endTime.split('.')

        startTime = int(startTime[0]) * 60 + int(startTime[1]) + startTimeOffset
        endTime = int(endTime[0]) * 60 + int(endTime[1]) + endTimeOffset

        now = now.hour * 60 + now.minute

        if self.date != None and now > endTime:
            return Status.OLD

        return Status.READY if now >= startTime and now <= endTime else Status.NOTYET

    def __str__(self) -> str:
        return f'{self.name[:20]}\n{self.time}'

    def jsonSerialize(self) -> dict:
        return {
            'name': self.name,
            'id': self.id,
            'password': self.password,
            'date': None if self.date == None else {
                'year': self.date.year,
                'month': self.date.month,
                'day': self.date.day
            },
            'weekDay': self.weekDay,
            'isFree': self.isFree,
            'time': self.time
        }

    def jsonDeserialize(meeting: dict) -> object:
        return Meeting(**meeting)