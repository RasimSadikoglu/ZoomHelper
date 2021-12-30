from datetime import datetime
from tkinter import Tk, ttk
import tkinter
from meeting import Meeting
from frames.schedule import weekDays

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
numberOfDaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class MeetingInfo(ttk.Frame):

    def __init__(self, master: Tk, meeting: Meeting=None):
        super().__init__(master)

        self.meeting = meeting

        self.initFrame()

        self.rowconfigure(1, weight=1)

        for i in range(2):
            self.columnconfigure(i, weight=1)

    def initFrame(self):
        ttk.Label(self, **{
            'text': 'Edit Meeting' if self.meeting != None else 'Add New Meeting',
            'anchor': 'center',
            'padding': 5
        }).grid(row=0, column=0, columnspan=3, sticky='ew', pady=10)

        self.infoFrame = InfoFrame(self, self.meeting)
        self.infoFrame.grid(row=1, column=0, rowspan=4, sticky='nes', padx=10, pady=10)

        self.dateFrame = DateFrame(self, self.meeting)
        self.dateFrame.grid(row=1, column=1, rowspan=4, sticky='news', padx=10, pady=10)

        ttk.Button(self, **{
            'text': 'Update' if self.meeting != None else 'Create',
            'command': self.updateMeeting,
            'padding': 10
        }).grid(row=2, column=2, padx=10, pady=15, sticky='sn')

        ttk.Button(self, **{
            'text': 'Cancel',
            'command': self.master.showMainMenu,
            'padding': 10
        }).grid(row=4, column=2, padx=10, pady=15, sticky='sn')

        if self.meeting != None:
            ttk.Button(self, **{
                'text': 'Delete',
                'command': self.deleteMeeting,
                'padding': 10
            }).grid(row=3, column=2, padx=10, pady=15, sticky='sn')

    def updateMeeting(self):
        meetingInfo = self.infoFrame.getValues()
        meetingDate = self.dateFrame.getValues()

        if self.meeting == None:
            self.master.meetings.append(Meeting(**meetingInfo, **meetingDate))
        else:
            self.meeting.update(**meetingInfo, **meetingDate)

        self.master.showMainMenu()

    def deleteMeeting(self):
        self.meeting.markForDelete = True
        self.master.showMainMenu()

class InfoFrame(ttk.Frame):

    def __init__(self, master: ttk.Frame, meeting: Meeting=None):
        super().__init__(master)

        self.name = tkinter.StringVar()
        self.id = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.link = tkinter.StringVar()

        if meeting != None:
            self.setValues(meeting)

        self.initFrame()

        # column, row = self.grid_size()

        # self.columnconfigure(1, weight=1)

        # for i in range(row):
        #     self.rowconfigure(i, weight=1)

    def initFrame(self):
        # Info Label
        ttk.Label(self, text='Meeting Info', anchor='center', padding=5).grid(row=0, column=0, columnspan=3, sticky='news')

        # Link Parser
        ttk.Label(self, text='Meeting Link', anchor='e', padding=5).grid(row=1, column=0, padx=5, pady=5, sticky='news')
        ttk.Entry(self, textvariable=self.link).grid(row=1, column=1, padx=5, pady=5, sticky='news')
        ttk.Button(self, text='Parse').grid(row=1, column=2, pady=5, sticky='news')

        # Meeting Name
        ttk.Label(self, text='Meeting Name', anchor='e', padding=5).grid(row=2, column=0, padx=5, pady=5, sticky='news')
        ttk.Entry(self, textvariable=self.name).grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='news')

        # Meeting ID
        ttk.Label(self, text='Meeting ID', anchor='e', padding=5).grid(row=3, column=0, padx=5, pady=5, sticky='news')
        ttk.Entry(self, textvariable=self.id).grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='news')

        # Meeting Password
        ttk.Label(self, text='Meeting Password', anchor='e', padding=5).grid(row=4, column=0, padx=5, pady=5, sticky='news')
        ttk.Entry(self, textvariable=self.password).grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='news')

    def getValues(self):
        return {
            'name': self.name.get(),
            'id': self.id.get(),
            'password': self.password.get()
        }

    def setValues(self, meeting: Meeting):
        self.name.set(meeting.name)
        self.id.set(meeting.id)
        self.password.set(meeting.password)

class DateFrame(ttk.Frame):

    def __init__(self, master: ttk.Frame, meeting: Meeting=None):
        super().__init__(master)

        self.isFree = False
        self.weeklyRepeat = tkinter.BooleanVar()
        self.weekDay = tkinter.StringVar()
        self.year, self.day = [tkinter.IntVar() for i in range(2)]
        self.month = tkinter.StringVar()
        self.startHour, self.startMinute, self.endHour, self.endMinute = [tkinter.IntVar() for i in range(4)]

        self.setValues(meeting)

        self.initFrame()

        # column, row = self.grid_size()

        # for i in range(column):
        #     self.columnconfigure(i, weight=1)

        # for i in range(row):
        #     self.rowconfigure(i, weight=1)

    def initFrame(self):
        ttk.Label(self, text='Meeting Date').grid(row=0, column=0, columnspan=4, pady=10)

        ttk.Label(self, text='Date', anchor='w').grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky='w')
        ttk.Checkbutton(self, text='Repeat Weekly', variable=self.weeklyRepeat, command=self.update).grid(row=1, column=2, columnspan=2)

        self.weekDayMenu = ttk.Combobox(self, textvariable=self.weekDay, values=weekDays, width=10)
        self.yearMenu = ttk.Combobox(self, textvariable=self.year, values=list(range(2021, 2026)), width=5)
        self.monthMenu = ttk.Combobox(self, textvariable=self.month, values=months, width=10)
        self.monthMenu.bind('<<ComboboxSelected>>', lambda e: self.updateDayMenu())

        self.dayMenu = ttk.Combobox(self, textvariable=self.day, width=5)
        self.updateDayMenu()

        ttk.Label(self, text='Start Time', anchor='w').grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky='w')
        ttk.Label(self, text='End Time', anchor='w').grid(row=3, column=2, columnspan=2, padx=5, pady=10, sticky='w')

        ttk.Combobox(self, textvariable=self.startHour, values=list(range(24)), width=5).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        ttk.Combobox(self, textvariable=self.startMinute, values=list(range(60)), width=5).grid(row=4, column=1, padx=5, pady=5, sticky='we')
        ttk.Combobox(self, textvariable=self.endHour, values=list(range(24)), width=5).grid(row=4, column=2, padx=5, pady=5, sticky='we')
        ttk.Combobox(self, textvariable=self.endMinute, values=list(range(60)), width=5).grid(row=4, column=3, padx=5, pady=5, sticky='e')

        self.update()

    def update(self):
        if self.weeklyRepeat.get():
            self.weekDayMenu.grid(row=2, column=0, columnspan=2, sticky='w')

            self.yearMenu.grid_remove()
            self.monthMenu.grid_remove()
            self.dayMenu.grid_remove()
        else:
            self.yearMenu.grid(row=2, column=0)
            self.monthMenu.grid(row=2, column=1, columnspan=2)
            self.dayMenu.grid(row=2, column=3)

            self.weekDayMenu.grid_remove()

    def updateDayMenu(self):
        numberOfDays = numberOfDaysInMonth[months.index(self.month.get())]

        numberOfDays += 1 if self.year.get() % 4 == 0 and self.month.get() == 'February' else 0

        self.dayMenu.configure(values=list(range(1, numberOfDays + 1)))

        if self.day.get() > numberOfDays:
            self.day.set(numberOfDays)

    def getValues(self):
        return {
            'date': datetime(year=self.year.get(), 
                    month=months.index(self.month.get()) + 1, 
                    day=self.day.get()).date() if not self.weeklyRepeat.get() else None,
            'weekDay': weekDays.index(self.weekDay.get()) if self.weeklyRepeat.get() else None,
            'isFree': False,
            'time': f'{self.startHour.get():02}.{self.startMinute.get():02}-{self.endHour.get():02}.{self.endMinute.get():02}'
        }

    def setValues(self, meeting: Meeting):
        now = datetime.now()

        if meeting == None:
            self.weeklyRepeat.set(True)
            self.weekDay.set(weekDays[now.weekday()])
            self.year.set(now.year)
            self.month.set(months[now.month - 1])
            self.day.set(now.day)
        else:
            self.weeklyRepeat.set(meeting.date == None)
            self.weekDay.set(weekDays[meeting.weekDay] if meeting.date == None and meeting.weekDay != None else weekDays[now.weekday()])
            self.year.set(meeting.date.year if meeting.date != None else now.year)
            self.month.set(months[meeting.date.month - 1] if meeting.date != None else months[now.month - 1])
            self.day.set(meeting.date.day if meeting.date != None else now.day)

            start, end = meeting.time.split('-')
            start, end = start.split('.'), end.split('.')

            self.startHour.set(int(start[0]))
            self.startMinute.set(int(start[1]))
            self.endHour.set(int(end[0]))
            self.endMinute.set(int(end[1]))

        if meeting == None or meeting.isFree:
            self.startHour.set(now.hour)
            self.startMinute.set(now.minute)
            self.endHour.set(now.hour)
            self.endMinute.set(now.minute)