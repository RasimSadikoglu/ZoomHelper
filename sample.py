from meeting import Meeting
import datetime
import sys
import json

meetings = []
timeout = 30

def read():
    data = open("data.txt", "r")

    ms = data.read().split("\n")
    ms.pop()

    for i in range(len(ms)):
        ms[i] = ms[i].split(" ")
        meetings.append(Meeting(ms[i][0], ms[i][1], ms[i][2], ms[i][3], ms[i][4]))

    print(ms)

def save():
    data = open("data.txt", "w")

    for m in meetings:
        data.write(m.print())

    data.close()

#def sort():
    
def config():
    read()

    op = input("1. ADD: ")

    while (op == "1"):
        meetings.append(Meeting(input("ID: "), input("PASSWORD: "), input("DAY: "), input("HOUR: "), input("MINUTE: ")))
        op = input("1. ADD: ")

    #sort()
    save()

def run():
    read()

    time = datetime.datetime.now()

    day = time.weekday()
    hour = time.hour
    minute = time.minute

    print("DOW: " + str(day) + "Hour: " + str(hour) + "Minute: " + str(minute))

    for m in meetings:
        print("\nM: " + m.print())

        if (day > int(m.day)):
            print("Wrong Day!\n")
            continue

        if (day == int(m.day) and (int(m.hour) - hour) * 60 + (int(m.minute) - minute) < timeout):
            print("Expired!\n")
            continue

        m.open()
        break

if (len(sys.argv) > 1 and (sys.argv[1] == "-config" or sys.argv[1] == "-c")):
    config()
else:
    run()