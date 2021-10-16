from meeting import Meeting
import datetime
import sys
from tkinter import *
from config import *

timeout = 30

def run():
    meetings = read()

    time = datetime.datetime.now()

    day = time.weekday()
    endTime = time.hour * 60 + time.minute

    for m in meetings:
        
        if (day != m["day"]):
            print(f"Wrong Day! ({Meeting.print(m)})\n")
            continue

        if (m["endTime"] - endTime < timeout):
            print(f"Expired! ({Meeting.print(m)})\n")
            continue

        Meeting.open(m)
        exit

def config():
    ZoomHelper()

def test():
    return

if (len(sys.argv) > 1 and (sys.argv[1] == "--config" or sys.argv[1] == "-c")):
    config()
elif (len(sys.argv) > 1 and sys.argv[1] == "--test"):
    test()
else:
    run()
