from os import system

class Meeting:

    def __init__(self, name, id, password, day, startTime, endTime):
        self.name = name
        self.id = id
        self.password = password
        self.day = day
        self.startTime = startTime
        self.endTime = endTime
    
    def open(self):
        system("%APPDATA%/Zoom/bin/Zoom.exe \"-url=zoommtg://zoom.us/join?action=join&confno={:s}&pwd={:s}\"".format(self["id"], self["password"]))

    def print(self):
        return "{:s} {:d} {:02d}.{:02d} - {:02d}.{:02d}".format(self["name"], self["day"], self["startTime"] // 60, self["startTime"] % 60, self["endTime"] // 60, self["endTime"] % 60)