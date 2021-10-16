import tkinter as tk
import json
import sys
import meeting as mt

from functools import cmp_to_key

weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

class ZoomHelper(tk.Frame):

    def __init__(self):
        super().__init__(tk.Tk())
        self.master.title("ZoomHelper")

        self.calendar()
        
        self.mainloop()

    def calendar(self):

        self.calendarFrame = tk.Frame(self.master)
        self.calendarFrame.pack()

        for x in range(7):
            tk.Label(self.calendarFrame, text=weekDays[x], borderwidth=2, relief="solid",
            width=15, height=2, padx=2, pady=2).grid(row=0, column=x)

        self.meetings = read()
        self.labels = []

        def deleteMeeting(index):
            self.meetings.remove(self.meetings[index])
            self.save()
            self.reset()

        count = [1, 1, 1, 1, 1, 1, 1]
        for i in range(len(self.meetings)):
            weekDay = self.meetings[i]["day"]

            self.labels.append(tk.Label(self.calendarFrame, text=mt.Meeting.info(self.meetings[i]), borderwidth=2,
            relief="solid", width=15, padx=2, pady=2, cursor="hand2"))

            self.labels[-1].grid(row=count[weekDay], column=weekDay)

            self.labels[-1].bind("<Button-1>", lambda e, index=i: self.meetingInfo(index, "Meeting Info"))
            self.labels[-1].bind("<Button-3>", lambda e, index=i: deleteMeeting(index))
            count[weekDay] += 1

        tk.Button(self.calendarFrame, text="ADD", command=lambda: self.meetingInfo(-1, "Add New Meeting")).grid(row=max(count) + 1, column=0)

    def meetingInfo(self, index, windowTitle):
        meetingInfoWindow = tk.Toplevel()
        meetingInfoWindow.title(windowTitle)

        tk.Label(meetingInfoWindow, text="Meeting Name: ", padx=5, pady= 5).grid(row=0, column=0)
        nameEntry = tk.Entry(meetingInfoWindow)
        nameEntry.grid(row=0, column=1, columnspan=2)
        if (index != -1):
            nameEntry.insert(0, self.meetings[index]["name"])

        tk.Label(meetingInfoWindow, text="ID: ", padx=5, pady=5).grid(row=1, column=0)
        idEntry = tk.Entry(meetingInfoWindow)
        idEntry.grid(row=1, column=1, columnspan=2)
        if (index != -1):
            idEntry.insert(0, self.meetings[index]["id"])

        tk.Label(meetingInfoWindow, text="Password: ", padx=5, pady=5).grid(row=2, column=0)
        passwordEntry = tk.Entry(meetingInfoWindow)
        passwordEntry.grid(row=2, column=1, columnspan=2)
        if (index != -1):
            passwordEntry.insert(0, self.meetings[index]["password"])

        tk.Label(meetingInfoWindow, text="Day of Week", padx=5, pady=5).grid(row=3, column=0)
        dayOfWeekMenu = tk.StringVar(meetingInfoWindow)
        if (index != -1):
            dayOfWeekMenu.set(weekDays[self.meetings[index]["day"]])
        tk.OptionMenu(meetingInfoWindow, dayOfWeekMenu, *weekDays).grid(row=4, column=0)

        tk.Label(meetingInfoWindow, text="Meeting Start", padx=5, pady=5).grid(row=3, column=1)
        startTimeEntry = tk.Entry(meetingInfoWindow, width=15)
        startTimeEntry.grid(row=4, column=1)
        if (index != -1):
            startTimeEntry.insert(0, mt.timeTranslate(self.meetings[index]["startTime"], 100))

        tk.Label(meetingInfoWindow, text="Meeting End", padx=5, pady=5).grid(row=3, column=2)
        endTimeEntry = tk.Entry(meetingInfoWindow, width=15)
        endTimeEntry.grid(row=4, column=2)
        if (index != -1):
            endTimeEntry.insert(0, mt.timeTranslate(self.meetings[index]["endTime"], 100))

        def add():
            meeting = {
                "name": "",
                "id": "",
                "password": "",
                "day": "",
                "startTime": 0,
                "endTime": 0
            }

            meeting["name"] = nameEntry.get()
            meeting["id"] = idEntry.get()
            meeting["password"] = passwordEntry.get()
            meeting["day"] = weekDays.index(dayOfWeekMenu.get())
            meeting["startTime"] = mt.timeTranslate(int(startTimeEntry.get()), 60)
            meeting["endTime"] = mt.timeTranslate(int(endTimeEntry.get()), 60)

            nameEntry.delete(0, tk.END)
            idEntry.delete(0, tk.END)
            passwordEntry.delete(0, tk.END)
            startTimeEntry.delete(0, tk.END)
            endTimeEntry.delete(0, tk.END)

            self.meetings.append(meeting)
            self.save()

        def update(delete):
            if (delete):
                self.meetings.remove(self.meetings[index])
            else:
                self.meetings[index]["name"] = nameEntry.get()
                self.meetings[index]["id"] = idEntry.get()
                self.meetings[index]["password"] = passwordEntry.get()
                self.meetings[index]["day"] = weekDays.index(dayOfWeekMenu.get())
                self.meetings[index]["startTime"] = mt.timeTranslate(int(startTimeEntry.get()), 60)
                self.meetings[index]["endTime"] = mt.timeTranslate(int(endTimeEntry.get()), 60)

            self.save()
            self.reset(meetingInfoWindow)

        if (index == -1):
            tk.Button(meetingInfoWindow, text="Add", pady=10, command=add).grid(row=5, column=0)
            tk.Button(meetingInfoWindow, text="Exit", pady=10, command=lambda: self.reset(meetingInfoWindow)).grid(row=5, column=2)
        else:
            tk.Button(meetingInfoWindow, text="Update", pady=10, command=lambda: update(False)).grid(row=5, column=0)
            tk.Button(meetingInfoWindow, text="Delete", pady=10, command=lambda: update(True)).grid(row=5, column=2)

    def reset(self, window=None):
        if (window != None):
            window.destroy()

        self.calendarFrame.destroy()

        self.calendar()

    def save(self):
        self.meetings = sorted(self.meetings, key=cmp_to_key(compare))

        with open(f'{sys.path[0]}/data.json', "w") as data:
            json.dump(self.meetings, data, default=lambda o: o.__dict__, indent=4)

def read():
    try:
        with open(f'{sys.path[0]}/data.json', "r") as data:
            return json.load(data)
    except:
        print('No JSON file found!')
        return []

def compare(m1, m2):
    if (m1["day"] != m2["day"]):
        return m1["day"] - m2["day"]

    return m1["startTime"] - m2["startTime"]