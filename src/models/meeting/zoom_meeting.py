from os import getenv, system
import subprocess, time, webbrowser, psutil
from sys import platform

from models.meeting.base_meeting import BaseMeeting


class ZoomMeeting(BaseMeeting):
    __id: int
    __password: str

    def __init__(self, name: str, id: int, password: str) -> None:
        super().__init__(name)

        self.__id = id
        self.__password = password

    def open_meeting(self) -> None:
        # TODO: refactor

        if platform in ["win32", "cygwin", "msys"]:
            zoomProcess = len(list(filter(lambda p: p.name() == "Zoom.exe", psutil.process_iter())))

            if zoomProcess == 0:
                subprocess.Popen([str(getenv("APPDATA")) + "/Zoom/bin/Zoom.exe"])
                time.sleep(5)

            url = f'{str(getenv("APPDATA")) + "/Zoom/bin/Zoom.exe"} "-url=zoommtg://zoom.us/join?action=join&confno={self.__id}&pwd={self.__password}"'
        elif platform == "darwin":
            url = f'open /Applications/zoom.us.app "--url=zoommtg://zoom.us/join?action=join&confno={self.__id}&pwd={self.__password}"'
        elif platform in ["linux", "linux2"]:
            zoomProcess = len(list(filter(lambda p: p.name() == "zoom", psutil.process_iter())))

            if zoomProcess == 0:
                subprocess.Popen(["zoom"])
                time.sleep(5)

            url = f'xdg-open "zoommtg://zoom.us/join?action=join&confno={self.__id}&pwd={self.__password}"'
        else:
            url = f"https://zoom.us/j/{self.__id}?pwd={self.__password}"
            webbrowser.open(url)
            return

        system(url)
