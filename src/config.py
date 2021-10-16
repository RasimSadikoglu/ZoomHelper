from functools import cmp_to_key
from tkinter import *
from meeting import Meeting
import json
import sys

weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

class ZoomHelper(Frame):
    
    def __init__(self):
        super().__init__(Tk())
        self.master.title("ZoomHelper")

        for x in range(7):
            Label(self.master, text=weekDays[x]).grid(row=0, column=x)

        self.meetings = read()

        count = [1, 1, 1, 1, 1, 1, 1]
        for meeting in self.meetings:
            weekDay = meeting["day"]
            Label(self.master, text=Meeting.info(meeting)).grid(row=count[weekDay], column=weekDay)
            count[weekDay] += 1

        Button(self.master, text="ADD", command=self.addNewMeeting).grid(row=max(count) + 1, column=0)

        self.mainloop()

    def addNewMeeting(self):

        addNewMeetingWindow = Toplevel()
        addNewMeetingWindow.title("Add New Meeting")

        Label(addNewMeetingWindow, text="Name: ", ).grid(row=0, column=0)
        name = Entry(addNewMeetingWindow)
        name.grid(row=0, column=1, columnspan=2)

        Label(addNewMeetingWindow, text="ID: ").grid(row=1, column=0)
        id = Entry(addNewMeetingWindow)
        id.grid(row=1, column=1, columnspan=2)

        Label(addNewMeetingWindow, text="Password: ").grid(row=2, column=0)
        password = Entry(addNewMeetingWindow)
        password.grid(row=2, column=1, columnspan=2)

        Label(addNewMeetingWindow, text="Day").grid(row=3, column=0)
        Label(addNewMeetingWindow, text="Start Time").grid(row=3, column=1)
        Label(addNewMeetingWindow, text="End Time").grid(row=3, column=2)

        day = Entry(addNewMeetingWindow)
        day.grid(row=4, column=0)

        startTime = Entry(addNewMeetingWindow)
        startTime.grid(row=4, column=1)

        endTime = Entry(addNewMeetingWindow)
        endTime.grid(row=4, column=2)

        def add():
            st = int(startTime.get())
            st = (st // 100) * 60 + (st % 100)

            et = int(endTime.get())
            et = (et // 100) * 60 + (et % 100)

            self.meetings.append({"name": name.get(), "id": id.get(), "password": password.get(), "day": int(day.get()), "startTime": st, "endTime": et})
            self.save()

            name.delete(0, END)
            id.delete(0, END)
            password.delete(0, END)
            day.delete(0, END)
            startTime.delete(0, END)
            endTime.delete(0, END)

        Button(addNewMeetingWindow, text="ADD", command=add).grid(row=5, column=0)
        Button(addNewMeetingWindow, text="EXIT", command=lambda: self.reset(addNewMeetingWindow)).grid(row=5, column=2)

    def reset(self, window):
        window.destroy()

        self.master.destroy()

        self.__init__()

    def save(self):
        self.meetings = sorted(self.meetings, key=cmp_to_key(compare))

        with open(f'{sys.path[0]}\data.json', "w") as data:
            json.dump(self.meetings, data, default=lambda o: o.__dict__, indent=4)

def read():
        try:
            with open(f'{sys.path[0]}\data.json', "r") as data:
                return json.load(data)
        except:
            print('No JSON file found!')
            return []

def compare(m1, m2):
    if (m1["day"] != m2["day"]):
        return m1["day"] - m2["day"]

    return m1["startTime"] - m2["startTime"]