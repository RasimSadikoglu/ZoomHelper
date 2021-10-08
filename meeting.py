from os import system

class Meeting:

    def __init__(self, id, password, day, hour, minute):
        self.id = id
        self.password = password
        self.day = day
        self.hour = hour
        self.minute = minute
    
    def open(self):
        system("%APPDATA%/Zoom/bin/Zoom.exe \"-url=zoommtg://zoom.us/join?action=join&confno={:s}&pwd={:s}\"".format(self.id, self.password))

    def print(self):
        return str(self.id) + " " + str(self.password) + " " + str(self.day) + " " + str(self.hour) + " " + str(self.minute) + "\n"