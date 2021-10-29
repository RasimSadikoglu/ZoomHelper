import tkinter, meeting
from tkinter import ttk

class DateFrame(ttk.Frame):

    def __init__(self, master, mt=None, det=False, r=True, isFree=False):
        super().__init__(master)
        self.grid(row=1)

        self.mt = mt

        self.differentEndTime = tkinter.BooleanVar()
        self.repetitive = tkinter.BooleanVar()
        self.isFree = isFree

        self.differentEndTime.set(det and not r)
        self.repetitive.set(r)

        labelTexts = ['Year', 'Month', 'Day', 'Hour', 'Minute']
        self.startLabels = [ttk.Label(self, text=t) for t in labelTexts]
        self.endLabels = [ttk.Label(self, text=t) for t in labelTexts]

        self.startDateEntries = [ttk.Entry(self, width=(4, 8)[t == 'Year']) for t in labelTexts]
        self.endDateEntries = [ttk.Entry(self, width=(4, 8)[t == 'Year']) for t in labelTexts]

        self.weekDayVar = tkinter.StringVar(self)
        self.weekdayMenu = ttk.OptionMenu(self, self.weekDayVar, *meeting.weekDays)

        if self.mt != None:
            self.insertInfo()

        if not self.isFree:
            self.placeIntoGrid()

    def insertInfo(self):

        startDate = [self.mt.startDate.year, self.mt.startDate.month, self.mt.startDate.day, self.mt.startDate.hour, self.mt.startDate.minute]
        endDate = [self.mt.endDate.year, self.mt.endDate.month, self.mt.endDate.day, self.mt.endDate.hour, self.mt.endDate.minute]

        for i in range(5):
            if self.mt.weekDay != -1 and i < 3:
                continue
            else:
                self.startDateEntries[i].insert(0, startDate[i])
                self.endDateEntries[i].insert(0, endDate[i])
        
        if self.mt.weekDay != -1:
            self.weekDayVar.set(meeting.weekDays[self.mt.weekDay])
            

    def placeIntoGrid(self):
        ttk.Label(self, text='Start Date:', width=16).grid(row=0, column=0, columnspan=2)
        ttk.Label(self, text='Weekly Repeat', width=24, anchor='e').grid(row=0, column=2, columnspan=3)
        
        ttk.Checkbutton(self, variable=self.repetitive, command=lambda: self.reset(self.isFree)).grid(row=0, column=5)

        ttk.Label(self, text='End Date:', width=16).grid(row=3, column=0, columnspan=2)
        ttk.Label(self, text='Different End Date', width=24, anchor='e').grid(row=3, column=2, columnspan=3)

        ttk.Checkbutton(self, variable=self.differentEndTime, state=('normal', 'disabled')[self.repetitive.get()], command=lambda: self.reset(self.isFree)).grid(row=3, column=5)

        self.startLabels[3].grid(row=1, column=3)
        self.startLabels[4].grid(row=1, column=4)
        self.startDateEntries[3].grid(row=2, column=3)
        self.startDateEntries[4].grid(row=2, column=4)

        self.endLabels[3].grid(row=4, column=3)
        self.endLabels[4].grid(row=4, column=4)
        self.endDateEntries[3].grid(row=5, column=3)
        self.endDateEntries[4].grid(row=5, column=4)

        if self.repetitive.get():
            self.startLabels[2].grid(row=1, columnspan=3)
            self.weekdayMenu.grid(row=2, columnspan=3)
        else:
            for i in range(2, -1, -1):
                self.startLabels[i].grid(row=1, column=2-i)
                self.startDateEntries[i].grid(row=2, column=2-i)

                if self.differentEndTime.get():
                    self.endLabels[i].grid(row=4, column=2-i)
                    self.endDateEntries[i].grid(row=5, column=2-i)
        

    def getValues(self):
        pass

    def reset(self, isFree):
        self.destroy()
        self.__init__(self.master, self.mt, self.differentEndTime.get(), self.repetitive.get(), isFree)