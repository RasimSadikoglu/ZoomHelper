import tkinter, meeting

class DateFrame(tkinter.Frame):

    def __init__(self, master, mt=None, det=False, r=True, isFree=False):
        super().__init__(master, background='white')
        self.grid(row=1)

        self.mt = mt

        self.differentEndTime = tkinter.BooleanVar()
        self.repetitive = tkinter.BooleanVar()
        self.isFree = isFree

        self.differentEndTime.set(det and not r)
        self.repetitive.set(r)

        labelTexts = ['Year', 'Month', 'Day', 'Hour', 'Minute']
        self.startLabels = [tkinter.Label(self, text=t, background='white', pady=3) for t in labelTexts]
        self.endLabels = [tkinter.Label(self, text=t, background='white', pady=3) for t in labelTexts]

        self.startDateEntries = [tkinter.Entry(self, width=(4, 8)[t == 'Year']) for t in labelTexts]
        self.endDateEntries = [tkinter.Entry(self, width=(4, 8)[t == 'Year']) for t in labelTexts]

        self.weekDayVar = tkinter.StringVar(self)
        self.weekdayMenu = tkinter.OptionMenu(self, self.weekDayVar, *meeting.weekDays)

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
        tkinter.Label(self, text='Start Date:', background='white', width=16, pady=10).grid(row=0, column=0, columnspan=2)
        tkinter.Label(self, text='Weekly Repeat', background='white', width=24, pady=10, anchor='e').grid(row=0, column=2, columnspan=3)
        
        tkinter.Checkbutton(self, background='white', variable=self.repetitive, command=lambda: self.reset(self.isFree)).grid(row=0, column=5)

        tkinter.Label(self, text='End Date:', background='white', width=16, pady=10).grid(row=3, column=0, columnspan=2)
        tkinter.Label(self, text='Different End Date', background='white', width=24, pady=10, anchor='e').grid(row=3, column=2, columnspan=3)

        tkinter.Checkbutton(self, background='white', variable=self.differentEndTime, state=('normal', 'disabled')[self.repetitive.get()], command=lambda: self.reset(self.isFree)).grid(row=3, column=5)

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
            for i in range(3):
                self.startLabels[2 - i].grid(row=1, column=i)
                self.startDateEntries[2 - i].grid(row=2, column=i)

                if self.differentEndTime.get():
                    self.endLabels[2 - i].grid(row=4, column=i)
                    self.endDateEntries[2 - i].grid(row=5, column=i)
        

    def getValues(self):
        pass

    def reset(self, isFree):
        self.destroy()
        self.__init__(self.master, self.mt, self.differentEndTime.get(), self.repetitive.get(), isFree)