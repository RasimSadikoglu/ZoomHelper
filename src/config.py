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

        self.isTherePopUp = False

        self.meetings = read()

        self.calendar()
        
        self.mainloop()
    
    def calendar(self):

        self.calendarFrame = tk.Frame(self.master, bg="white")
        self.calendarFrame.pack()

        for x in range(7):
            tk.Label(self.calendarFrame, text=weekDays[x], borderwidth=1, relief="solid",
            width=15, height=2, padx=2, pady=2, bg="white", fg="black").grid(row=0, column=x)

        self.labels = []

        def deleteMeeting(index):
            if (not self.isTherePopUp):
                self.meetings.remove(self.meetings[index])
                self.reset()

        data = read()

        count = [1, 1, 1, 1, 1, 1, 1]
        for i in range(len(self.meetings)):
            weekDay = self.meetings[i]["day"]

            self.labels.append(tk.Label(self.calendarFrame, text=mt.Meeting.info(self.meetings[i]), borderwidth=1,
            relief="solid", width=15, padx=2, pady=2, cursor="hand2", bg=("yellow", "white")[self.meetings[i] in data], fg="black"))

            self.labels[-1].grid(row=count[weekDay], column=weekDay)

            self.labels[-1].bind("<Button-1>", lambda e, index=i: self.meetingInfo(index, "Meeting Info"))
            self.labels[-1].bind("<Button-3>", lambda e, index=i: deleteMeeting(index))
            count[weekDay] += 1

        tk.Button(self.calendarFrame, cursor="hand2", height=2, width=14, relief="solid", borderwidth=1, text="Add", 
        command=lambda: self.meetingInfo(-1, "Add New Meeting")).grid(row=max(count) + 1, column=0)

        tk.Button(self.calendarFrame, cursor="hand2", height=2, width=14, relief="solid", borderwidth=1, text="Revert", 
        command=lambda: self.reset(load=True)).grid(row=max(count) + 1, column=3)

        tk.Button(self.calendarFrame, cursor="hand2", height=2, width=14, relief="solid", borderwidth=1, text="Save", 
        command=self.save).grid(row=max(count) + 1, column=6)

    def meetingInfo(self, index, windowTitle):
        if (self.isTherePopUp):
            return

        meetingInfoWindow = tk.Toplevel()
        meetingInfoWindow.title(windowTitle)

        self.isTherePopUp = True
        meetingInfoWindow.protocol("WM_DELETE_WINDOW", lambda: self.reset(window=meetingInfoWindow))

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

            self.meetings = sorted(self.meetings, key=cmp_to_key(compare))

            self.reset()

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

            self.meetings = sorted(self.meetings, key=cmp_to_key(compare))

            self.reset(meetingInfoWindow)

        if (index == -1):
            tk.Button(meetingInfoWindow, text="Add", pady=10, command=add).grid(row=5, column=0)
            tk.Button(meetingInfoWindow, text="Exit", pady=10, command=lambda: self.reset(meetingInfoWindow)).grid(row=5, column=2)
        else:
            tk.Button(meetingInfoWindow, text="Update", pady=10, command=lambda: update(False)).grid(row=5, column=0)
            tk.Button(meetingInfoWindow, text="Delete", pady=10, command=lambda: update(True)).grid(row=5, column=2)

    def reset(self, window=None, load=False):
        if (window != None):
            self.isTherePopUp = False
            window.destroy()

        if (load and not self.isTherePopUp):
            self.meetings = read()

        self.calendarFrame.destroy()

        self.calendar()

    def save(self):
        # self.meetings = sorted(self.meetings, key=cmp_to_key(compare))

        if (self.isTherePopUp):
            return

        with open(f'{sys.path[0]}/data.json', "w") as data:
            json.dump(self.meetings, data, default=lambda o: o.__dict__, indent=4)

        self.reset()

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