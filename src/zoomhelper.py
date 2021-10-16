import config as cnf
import meeting

import datetime
import sys

timeout = 30

def run():
    meetings = cnf.read()

    time = datetime.datetime.now()

    day = time.weekday()
    endTime = time.hour * 60 + time.minute

    for m in meetings:
        
        if (day != m["day"]):
            print(f"Wrong Day! ({meeting.Meeting.print(m)})\n")
            continue

        if (m["endTime"] - endTime < timeout):
            print(f"Expired! ({meeting.Meeting.print(m)})\n")
            continue

        meeting.Meeting.open(m)
        exit

def config():
    cnf.ZoomHelper()

def test():
    return

if (len(sys.argv) > 1 and (sys.argv[1] == "--config" or sys.argv[1] == "-c")):
    config()
elif (len(sys.argv) > 1 and sys.argv[1] == "--test"):
    test()
else:
    run()
