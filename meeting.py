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
        system("%APPDATA%/Zoom/bin/Zoom.exe \"-url=zoommtg://zoom.us/join?action=join&confno={:s}&pwd={:s}\"".format(self.id, self.password))

    def print(self):
        return str(self.id) + " " + str(self.password) + " " + str(self.day) + " " + str(self.endTime) + " " + "\n"