from tkinter import *
from tkinter import ttk

from meeting import Meeting

def main():
    return

def addNewMeeting():
    meetings = []

    root = Tk()
    root.title("ZoomHelper")

    frm = ttk.Frame(root, padding=10).grid()

    ttk.Label(frm, text="Name: ", ).grid(row=0, column=0)
    name = ttk.Entry(frm)
    name.grid(row=0, column=1, columnspan=2)

    ttk.Label(frm, text="ID: ").grid(row=1, column=0)
    id = ttk.Entry(frm)
    id.grid(row=1, column=1, columnspan=2)

    ttk.Label(frm, text="Password: ").grid(row=2, column=0)
    password = ttk.Entry(frm)
    password.grid(row=2, column=1, columnspan=2)

    ttk.Label(frm, text="Day").grid(row=3, column=0)
    ttk.Label(frm, text="Start Time").grid(row=3, column=1)
    ttk.Label(frm, text="End Time").grid(row=3, column=2)

    day = ttk.Entry(frm)
    day.grid(row=4, column=0)

    startTime = ttk.Entry(frm)
    startTime.grid(row=4, column=1)

    endTime = ttk.Entry(frm)
    endTime.grid(row=4, column=2)

    def add():
        st = int(startTime.get())
        st = (st // 100) * 60 + (st % 100)

        et = int(endTime.get())
        et = (et // 100) * 60 + (et % 60)

        meetings.append(Meeting(name.get(), id.get(), password.get(), int(day.get()), st, et))

        name.delete(0, END)
        id.delete(0, END)
        password.delete(0, END)
        day.delete(0, END)
        startTime.delete(0, END)
        endTime.delete(0, END)

    ttk.Button(frm, text="ADD", command=add).grid(row=5, column=0)
    ttk.Button(frm, text="EXIT", command=root.destroy).grid(row=5, column=2)

    root.mainloop()

    return meetings