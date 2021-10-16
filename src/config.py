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

        for x in range(7):
            tk.Label(self.master, text=weekDays[x], borderwidth=2, relief="solid",
            width=15, height=2, padx=2, pady=2).grid(row=0, column=x)

        self.meetings = read()
        self.labels = []

        count = [1, 1, 1, 1, 1, 1, 1]
        for i in range(len(self.meetings)):
            weekDay = self.meetings[i]["day"]

            self.labels.append(tk.Label(self.master, text=mt.Meeting.info(self.meetings[i]), borderwidth=2,
            relief="solid", width=15, padx=2, pady=2, cursor="hand2"))

            self.labels[-1].grid(row=count[weekDay], column=weekDay)

            self.labels[-1].bind("<Button-1>", lambda e, index=i: self.meetingInfo(index))
            count[weekDay] += 1

        tk.Button(self.master, text="ADD", command=self.addNewMeeting).grid(row=max(count) + 1, column=0)

        self.mainloop()

    def addNewMeeting(self):

        addNewMeetingWindow = tk.Toplevel()
        addNewMeetingWindow.title("Add New Meeting")

        tk.Label(addNewMeetingWindow, text="Name: ", ).grid(row=0, column=0)
        name = tk.Entry(addNewMeetingWindow)
        name.grid(row=0, column=1, columnspan=2)

        tk.Label(addNewMeetingWindow, text="ID: ").grid(row=1, column=0)
        id = tk.Entry(addNewMeetingWindow)
        id.grid(row=1, column=1, columnspan=2)

        tk.Label(addNewMeetingWindow, text="Password: ").grid(row=2, column=0)
        password = tk.Entry(addNewMeetingWindow)
        password.grid(row=2, column=1, columnspan=2)

        tk.Label(addNewMeetingWindow, text="Day").grid(row=3, column=0)
        tk.Label(addNewMeetingWindow, text="Start Time").grid(row=3, column=1)
        tk.Label(addNewMeetingWindow, text="End Time").grid(row=3, column=2)

        day = tk.Entry(addNewMeetingWindow)
        day.grid(row=4, column=0)

        startTime = tk.Entry(addNewMeetingWindow)
        startTime.grid(row=4, column=1)

        endTime = tk.Entry(addNewMeetingWindow)
        endTime.grid(row=4, column=2)

        def add():
            st = int(startTime.get())
            st = (st // 100) * 60 + (st % 100)

            et = int(endTime.get())
            et = (et // 100) * 60 + (et % 100)

            self.meetings.append({"name": name.get(), "id": id.get(), "password": password.get(), "day": int(day.get()), "startTime": st, "endTime": et})
            self.save()

            name.delete(0, tk.END)
            id.delete(0, tk.END)
            password.delete(0, tk.END)
            day.delete(0, tk.END)
            startTime.delete(0, tk.END)
            endTime.delete(0, tk.END)

        tk.Button(addNewMeetingWindow, text="ADD", command=add).grid(row=5, column=0)
        tk.Button(addNewMeetingWindow, text="EXIT", command=lambda: self.reset(addNewMeetingWindow)).grid(row=5, column=2)

    def meetingInfo(self, index):
        meetingInfoWindow = tk.Toplevel()
        meetingInfoWindow.title("Meeting Info")

        tk.Label(meetingInfoWindow, text="Meeting Name: ", padx=5, pady= 5).grid(row=0, column=0)
        nameEntry = tk.Entry(meetingInfoWindow)
        nameEntry.grid(row=0, column=1, columnspan=2)
        nameEntry.insert(0, self.meetings[index]["name"])

        tk.Label(meetingInfoWindow, text="ID: ", padx=5, pady=5).grid(row=1, column=0)
        idEntry = tk.Entry(meetingInfoWindow)
        idEntry.grid(row=1, column=1, columnspan=2)
        idEntry.insert(0, self.meetings[index]["id"])

        tk.Label(meetingInfoWindow, text="Password: ", padx=5, pady=5).grid(row=2, column=0)
        passwordEntry = tk.Entry(meetingInfoWindow)
        passwordEntry.grid(row=2, column=1, columnspan=2)
        passwordEntry.insert(0, self.meetings[index]["password"])

        tk.Label(meetingInfoWindow, text="Day of Week", padx=5, pady=5).grid(row=3, column=0)
        dayOfWeekMenu = tk.StringVar(meetingInfoWindow)
        dayOfWeekMenu.set(weekDays[self.meetings[index]["day"]])
        tk.OptionMenu(meetingInfoWindow, dayOfWeekMenu, *weekDays).grid(row=4, column=0)

        def update(delete):
            if (delete):
                self.meetings.remove(self.meetings[index])
            else:
                self.meetings[index]["name"] = nameEntry.get()
                self.meetings[index]["id"] = idEntry.get()
                self.meetings[index]["password"] = passwordEntry.get()
                self.meetings[index]["day"] = weekDays.index(dayOfWeekMenu.get())
                # self.meetings[index]["startTime"] = startTimeEntry.get()
                # self.meetings[index]["endTime"] = endTimeEntry.get()

            self.save()
            self.reset(meetingInfoWindow)


        tk.Button(meetingInfoWindow, text="Update", command=lambda: update(False)).grid(row=5, column=0)
        tk.Button(meetingInfoWindow, text="Delete", command=lambda: update(True)).grid(row=5, column=2)

    def reset(self, window=None):
        if (window != None):
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