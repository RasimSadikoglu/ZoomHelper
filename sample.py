from meeting import Meeting
import datetime
import sys
import json
from tkinter import *
import GUI

timeout = 30

def read():
    with open("data.json", "r") as data:
        return json.load(data)

def save(meetings):
    with open("data.json", "w") as data:
        json.dump(meetings, data, default=lambda o: o.__dict__, indent=4)
    
def config():

    meetings = read()

    meetings = GUI.addNewMeeting(meetings)

    save(meetings)

def run():
    meetings = read()

    time = datetime.datetime.now()

    day = time.weekday()
    endTime = time.hour * 60 + time.minute

    for m in meetings:
        
        if (day != m["day"]):
            print("Wrong Day! ({:s})\n".format(Meeting.print(m)))
            continue

        if (m["endTime"] - endTime < timeout):
            print("Expired!\n")
            continue

        Meeting.open(m)
        break

def test():
    GUI.addNewMeeting()
    return

if (len(sys.argv) > 1 and (sys.argv[1] == "-config" or sys.argv[1] == "-c")):
    config()
elif (len(sys.argv) > 1 and sys.argv[1] == "-test"):
    test()
else:
    run()