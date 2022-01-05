from tkinter import ttk
from datetime import datetime, timedelta
from .schedule import Schedule
from meeting.meeting import Meeting
from dataio import data
from updater import getLocalVersion

class MainMenu(ttk.Frame):

    def __init__(self, master, meetings: list[Meeting], jsonData: list[dict]):
        super().__init__(master)

        self.meetings, self.jsonData = meetings, jsonData

        self.timeWindow = self.setTimeWindow(0)

        self.schedule = Schedule(self, meetings, jsonData, self.timeWindow)
        column, row = self.schedule.grid_size()
        self.row = max(row, 4)
        self.schedule.grid(column=0, row=1, sticky='news', columnspan=column, rowspan=self.row)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.initMainMenu()

    def setTimeWindow(self, offset: int, timeWindow=None) -> dict:
        now = datetime.now().date()
        weekDay = now.weekday()
        
        if timeWindow == None:
            return {
                'begin': now + timedelta(days=-weekDay),
                'end': now + timedelta(days=6-weekDay)
            }

        if offset == 0:
            timeWindow.update({
                'begin': now + timedelta(days=-weekDay),
                'end': now + timedelta(days=6-weekDay)
            })
        else:
            timeWindow['begin'] += timedelta(days=offset)
            timeWindow['end'] += timedelta(days=offset)

        self.schedule.update()
        return timeWindow

    def initMainMenu(self):
        
        # Left Button
        ttk.Button(self, **{
            'text': '<',
            'command': lambda: self.setTimeWindow(-7, self.timeWindow),
            'padding': 5,
        }).grid(**{
            'row': 0,
            'column': 0,
            'padx': 10,
            'pady': 5,
            'sticky': 'w'
        })

        # Date Label
        dateLabel = ttk.Label(self, **{
            'text': datetime.today().strftime('%d %B, %Y - %A'),
            'anchor': 'center',
            'cursor': 'hand2'
        })
        dateLabel.grid(**{
            'row': 0,
            'column': 1,
            'padx': 10,
            'pady': 5,
            'sticky': 'we',
            'columnspan': 5
        })
        dateLabel.bind('<Button-1>', lambda e: self.setTimeWindow(0, self.timeWindow))

        # Right Button
        ttk.Button(self, **{
            'text': '>',
            'command': lambda: self.setTimeWindow(7, self.timeWindow),
            'padding': 5,
        }).grid(**{
            'row': 0,
            'column': 6,
            'padx': 10,
            'pady': 5,
            'sticky': 'e'
        })

        ttk.Button(self, text='Other Meetings', padding=5).grid(row=self.row + 2, column=0, padx= 10, pady=10, sticky='e')
        ttk.Label(self, text='Left Click for Edit, Right Click for Delete', anchor='center').grid(row=self.row + 3, column=0, columnspan=8, pady=10)
        ttk.Label(self, text=getLocalVersion(), anchor='w').grid(row=self.row + 3, column=7, pady=10, padx=5, sticky='e')

        ttk.Button(self, text='Save', padding=5, command=lambda: self.save()).grid(row=self.row, column=7, padx=5, pady=5, sticky='se')
        ttk.Button(self, text='Revert', padding=5, command=lambda: self.revert()).grid(row=self.row - 1, column=7, padx=5, pady=5, sticky='se')
        ttk.Button(self, text='Add', padding=5, command=self.meetingInfo).grid(row=self.row - 2, column=7, padx=5, pady=5, sticky='se')

        self.unSavedLabel = ttk.Label(self, text='There are unsaved changes! Please revert or save before exit!', foreground='red', anchor='center')

        ttk.Button(self, text='Settings', padding=5, command=self.master.settings).grid(row=0, column=7, padx=5, pady=5, sticky='ne')

    def exitCheck(self):
        if not self.schedule.changes:
            return True

        self.unSavedLabel.grid(row=self.row + 4, column=0, columnspan=8, pady=10)

        self.after(5000, self.unSavedLabel.grid_remove)

    def revert(self):
        self.meetings.clear()

        for m in self.jsonData:
            self.meetings.append(Meeting.jsonDeserialize(m))

        self.schedule.update()

    def save(self):
        self.jsonData.clear()

        for m in self.meetings:
            if not m.markForDelete:
                self.jsonData.append(m.jsonSerialize())

        self.meetings.clear()

        for jd in self.jsonData:
            self.meetings.append(Meeting.jsonDeserialize(jd))

        data.saveDataFile(self.meetings)

        self.schedule.update()

    def meetingInfo(self, meeting=None):
        self.master.meetingInfo(meeting)