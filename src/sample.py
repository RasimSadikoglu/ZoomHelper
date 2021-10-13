from meeting import Meeting
import datetime
import sys
import json
from tkinter import *
import GUI
from functools import cmp_to_key

timeout = 30

def read():
    with open("data.json", "r") as data:
        return json.load(data)

def save(meetings):
    with open("data.json", "w") as data:
        json.dump(meetings, data, default=lambda o: o.__dict__, indent=4)

def compare(m1, m2):
    if (m1["day"] != m2["day"]):
        return m1["day"] - m2["day"]

    return m1["endTime"] - m2["endTime"]
    
def config():
    try:
        meetings = read()
    except:
        meetings = []
    
    meetings.extend(GUI.addNewMeeting())

    meetings = sorted(meetings, key=cmp_to_key(compare))

    save(meetings)

def run():
    try:
        meetings = read()
    except:
        print("No data file!\n")
        exit

    time = datetime.datetime.now()

    day = time.weekday()
    endTime = time.hour * 60 + time.minute

    for m in meetings:
        
        if (day != m["day"]):
            print(f"Wrong Day! ({Meeting.print(m)})\n")
            continue

        if (m["endTime"] - endTime < timeout):
            print("Expired!\n")
            continue

        Meeting.open(m)
        exit

def test():
    sorted(read(), key=cmp_to_key(compare))
    return

if (len(sys.argv) > 1 and (sys.argv[1] == "--config" or sys.argv[1] == "-c")):
    config()
elif (len(sys.argv) > 1 and sys.argv[1] == "--test"):
    test()
else:
    run()
