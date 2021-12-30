from tkinter import ttk
from meeting import Meeting
from datetime import datetime, timedelta

weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class MeetingColor(enumerate):
    UPDATE='#E8FF89'
    DELETE='#FF5A40'
    SAME='white'

class Schedule(ttk.Frame):

    def __init__(self, master: ttk.Frame, meetings: list[Meeting], jsonData: list[dict], timeWindow: dict):
        super().__init__(master, padding=5)

        self.meetings, self.jsonData = meetings, jsonData
        self.timeWindow = timeWindow

        self.initGrid()
        
        column, row = self.grid_size()

        for i in range(row):
            self.rowconfigure(i, weight=1)

        for i in range(column):
            self.columnconfigure(i, weight=1)

    def initGrid(self):
        self.changes = False

        grid = [[] for i in range(7)]

        for m in sorted(self.meetings, key=lambda x: (x.date.weekday() if x.date != None else x.weekDay, x.time)):

            if m.date != None and not (m.date >= self.timeWindow['begin'] and m.date <= self.timeWindow['end']):
                continue

            weekDay = m.date.weekday() if m.date != None else m.weekDay
            grid[weekDay].append(m)

        self.placeGrid(grid)

    def placeGrid(self, grid: list[list[Meeting]]):
        today = self.timeWindow['begin']

        for w, i in zip(weekDays, range(len(weekDays))):
            ttk.Label(self, **{
                'text': f'{w}\n{str(today)}',
                'padding': 5,
                'relief': 'solid',
                'anchor': 'center',
                'background': '#69E7FF' if today == datetime.now().date() else 'white'
            }).grid(**{
                'row': 0,
                'column': i,
                'padx': 5,
                'pady': 5,
                'sticky': 'news'
            })

            today += timedelta(days=1)

        def meetingColor(meeting: Meeting):
            if meeting.markForDelete:
                self.changes = True
                return MeetingColor.DELETE

            if meeting.jsonSerialize() not in self.jsonData:
                self.changes = True
                return MeetingColor.UPDATE

            return MeetingColor.SAME

        for day, column in zip(grid, range(len(grid))):
            for meeting, row in zip(day, range(1, len(day) + 1)):

                meetingLabel = ttk.Label(self, **{
                    'text': str(meeting),
                    'padding': 5,
                    'relief': 'solid',
                    'anchor': 'center',
                    'background': meetingColor(meeting),
                    'cursor': 'hand2'
                })

                meetingLabel.grid(**{
                    'row': row,
                    'column': column,
                    'padx': 5,
                    'pady': 5,
                    'sticky': 'news'
                })

                meetingLabel.bind('<Button-1>', lambda e, m=meeting: self.master.meetingInfo(m))
                meetingLabel.bind('<Button-3>', lambda e, m=meeting: self.deleteMeeting(m))

    def deleteMeeting(self, meeting: Meeting):
        meeting.markForDelete ^= True
        self.update()

    def update(self):
        for child in self.winfo_children():
            child.destroy()

        self.initGrid()

        column, row = self.grid_size()

        for i in range(row):
            self.rowconfigure(i, weight=1)

        for i in range(column):
            self.columnconfigure(i, weight=1)