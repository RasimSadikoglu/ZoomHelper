from os import system

weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

class Meeting:
    
    def open(self):
        system("%APPDATA%/Zoom/bin/Zoom.exe \"-url=zoommtg://zoom.us/join?action=join&confno={:s}&pwd={:s}\"".format(self["id"], self["password"]))

    def info(self):
        st = self["startTime"]
        et = self["endTime"]

        startTime = f'{st // 60:02}.{st % 60:02}'
        endTime = f'{et // 60:02}.{et % 60:02}'

        return f'{self["name"]}\n{weekDays[self["day"]]}\n{startTime} - {endTime}'

    def print(self):
        return f'{self["name"]} {weekDays[self["day"]]} {self["startTime"] // 60:02}.{self["startTime"] % 60:02} - {self["endTime"] // 60:02}.{self["endTime"] % 60:02}'

def timeTranslate(time, targetBase):
    if (targetBase == 100):
        return (time // 60) * 100 + (time % 60)
    elif (targetBase == 60):
        return (time // 100) * 60 + (time % 100)