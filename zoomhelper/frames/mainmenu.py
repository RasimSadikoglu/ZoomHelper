from tkinter import ttk
from frames.schedule import Schedule
from datetime import datetime, timedelta

class MainMenu(ttk.Frame):

    def __init__(self, master, meetings: list):
        super().__init__(master)

        self.meetings = meetings

        self.timeWindow = self.setTimeWindow(0)

        self.initMainMenu()

        self.schedule = Schedule(self, meetings, self.timeWindow)
        self.schedule.grid(row=1, sticky='news', columnspan=3)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

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

        buttonOptions = {
            'text': '<',
            'command': lambda: self.setTimeWindow(-7, self.timeWindow),
            'padding': 5,
        }

        gridOptins = {
            'row': 0,
            'column': 0,
            'padx': 10,
            'pady': 5,
            'sticky': 'w'
        }
        
        ttk.Button(self, **buttonOptions).grid(**gridOptins)

        gridOptins.update({
            'column': 1,
            'sticky': 'we'
        })

        dateLabel = ttk.Label(self, **{
            'text': datetime.today().strftime('%d %B, %Y - %A'),
            'anchor': 'center',
            'cursor': 'hand2'
        })
        dateLabel.grid(**gridOptins)
        dateLabel.bind('<Button-1>', lambda e: self.setTimeWindow(0, self.timeWindow))

        buttonOptions.update({
            'text': '>',
            'command': lambda: self.setTimeWindow(7, self.timeWindow)
        })

        gridOptins.update({
            'column': 2,
            'sticky': 'e'
        })

        ttk.Button(self, **buttonOptions).grid(**gridOptins)