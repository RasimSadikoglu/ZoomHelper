from typing import DefaultDict
from meeting import Meeting
import datetime
import sys
import json
from tkinter import *

timeout = 30

def read():
    with open("data.json", "r") as data:
        global meetings
        meetings = json.load(data)

def save():
    with open("data.json", "w") as data:
        json.dump(meetings, data, default=lambda o: o.__dict__, indent=4)
    
def config():
    read()

    root = Tk()

    nameInput = Entry(root, width=40)
    idInput = Entry(root, width=40)
    passwordInput = Entry(root, width=40)
    dayInput = Entry(root, width=10)
    starTimeInput = Entry(root, width=15)
    endTimeInput = Entry(root, width=15)

    def addMeeting():
        meetings.append(Meeting(nameInput.get(), idInput.get(), passwordInput.get(), dayInput.get(), starTimeInput.get(), endTimeInput.get()))

    addButton = Button(root, text="ADD", padx=15, pady=5, command=addMeeting)
    exitButton = Button(root, text="EXIT", padx=15, pady=5, command=root.destroy)
    
    nameInput.grid(row=0, columnspan=3)
    idInput.grid(row=1, columnspan=3)
    passwordInput.grid(row=2, columnspan=3)
    dayInput.grid(row=3, column=0)
    starTimeInput.grid(row=3, column=1)
    endTimeInput.grid(row=3, column=2)
    addButton.grid(row=4, column=0)
    exitButton.grid(row=4, column=2)
    root.mainloop()

    save()

def run():
    read()

    time = datetime.datetime.now()

    day = time.weekday()
    endTime = time.hour * 100 + time.minute

    for m in meetings:
        
        if (day != int(m["day"])):
            print("Wrong Day!\n")
            continue

        if (int(m.endTime) - endTime < timeout):
            print("Expired!\n")
            continue

        m.open()
        break

def test():
    return

if (len(sys.argv) > 1 and (sys.argv[1] == "-config" or sys.argv[1] == "-c")):
    config()
elif (len(sys.argv) > 1 and sys.argv[1] == "-test"):
    test()
else:
    run()