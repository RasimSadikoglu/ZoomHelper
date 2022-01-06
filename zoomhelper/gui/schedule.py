from sys import platform
from tkinter import ttk
from meeting.meeting import Meeting
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
        self.otherMeetingsIndex = 0
        self.otherMeetings = False

        self.initGrid()
        
        column, row = self.grid_size()

        for i in range(1, row):
            self.rowconfigure(i, weight=1)

        for i in range(column):
            self.columnconfigure(i, weight=1)

    def initGrid(self):
        self.changes = False

        grid = [[] for i in range(7)]
        otherMeetings = []

        for m in sorted(self.meetings, key=lambda x: (x.date.weekday() if x.date != None else x.weekDay, x.time)):

            if m.isFree or m.date != None:
                otherMeetings.append(m)
            
            if m.isFree:
                continue

            if m.date != None and not (m.date >= self.timeWindow['begin'] and m.date <= self.timeWindow['end']):
                continue

            weekDay = m.date.weekday() if m.date != None else m.weekDay
            grid[weekDay].append(m)

        if self.otherMeetings:
            self.initOtherMeetings(otherMeetings)
        else:
            self.placeGrid(grid)

    def placeGrid(self, grid: list[list[Meeting]]):
        today = self.timeWindow['begin']

        for i, w in enumerate(weekDays):
            ttk.Label(self, **{
                'text': f'{w}\n{str(today)}',
                'padding': 5,
                'relief': 'solid',
                'width': 15,
                'anchor': 'n',
                'background': '#235c82' if today == datetime.now().date() else '#70a7cc',
                'foreground': 'white' if today == datetime.now().date() else 'black'
            }).grid(**{
                'row': 0,
                'column': i,
                'padx': 5,
                'pady': 5,
                'sticky': 'ew'
            })

            today += timedelta(days=1)

        for column, day in enumerate(grid):
            for row, meeting in enumerate(day, 1):

                meetingLabel = ttk.Label(self, **{
                    'text': str(meeting),
                    'padding': 5,
                    'relief': 'solid',
                    'anchor': 'center',
                    'background': self.meetingColor(meeting),
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
                if platform == "darwin":
                    meetingLabel.bind('<Button-2>', lambda e, m=meeting: self.deleteMeeting(m))
                else:
                    meetingLabel.bind('<Button-3>', lambda e, m=meeting: self.deleteMeeting(m))
    
    def meetingColor(self, meeting: Meeting):
        if meeting.markForDelete:
            self.changes = True
            return MeetingColor.DELETE

        if meeting.jsonSerialize() not in self.jsonData:
            self.changes = True
            return MeetingColor.UPDATE

        return MeetingColor.SAME

    def initOtherMeetings(self, otherMeetings: list[Meeting]):
        freeMeetings = list(filter(lambda m: m.isFree, otherMeetings))
        otherMeetings = list(filter(lambda m: not m.isFree, otherMeetings))

        grid = {}

        if len(freeMeetings) != 0:
            grid['Free\n'] = freeMeetings

        for m in otherMeetings:
            date = f'{m.date.year:04}-{m.date.month:02}-{m.date.day:02}'

            if date in grid:
                grid[date].append(m)
            else:
                grid[date] = [m]

        self.placeOtherMeetings(grid)

    def placeOtherMeetings(self, otherMeetings: dict):
        
        otherMeetings = sorted(otherMeetings.items())

        if self.otherMeetingsIndex >= len(otherMeetings):
            self.otherMeetingsIndex -= 7
        if self.otherMeetingsIndex < 0:
            self.otherMeetingsIndex = 0

        grid = otherMeetings[self.otherMeetingsIndex:]

        grid = grid[:7]

        for i, (date, meetings) in enumerate(grid):
            dateObject = None
            
            if date != 'Free\n':
                dateList = date.split('-')
                dateObject = datetime(year=int(dateList[0]), month=int(dateList[1]), day=int(dateList[2])).date()
                weekDay = weekDays[dateObject.weekday()]

                date = weekDay + '\n' + date

                meetings = sorted(meetings, key=lambda m: m.time)

            ttk.Label(self, **{
                'text': date,
                'padding': 5,
                'relief': 'solid',
                'width': 15,
                'anchor': 'n',
                'background': '#235c82' if dateObject == datetime.now().date() else '#70a7cc',
                'foreground': 'white' if dateObject == datetime.now().date() else 'black'
            }).grid(**{
                'row': 0,
                'column': i,
                'padx': 5,
                'pady': 5,
                'sticky': 'ew'
            })

            for j, meeting in enumerate(meetings, 1):
                meetingLabel = ttk.Label(self, **{
                    'text': str(meeting),
                    'padding': 5,
                    'relief': 'solid',
                    'anchor': 'center',
                    'background': self.meetingColor(meeting),
                    'cursor': 'hand2'
                })

                meetingLabel.grid(**{
                    'row': j,
                    'column': i,
                    'padx': 5,
                    'pady': 5,
                    'sticky': 'news'
                })

                meetingLabel.bind('<Button-1>', lambda e, m=meeting: self.master.meetingInfo(m))
                if platform == "darwin":
                    meetingLabel.bind('<Button-2>', lambda e, m=meeting: self.deleteMeeting(m))
                else:
                    meetingLabel.bind('<Button-3>', lambda e, m=meeting: self.deleteMeeting(m))

        for i in range(len(grid),7):
            ttk.Label(self, **{
                'text': 'XXXX\nXXXX',
                'padding': 5,
                'relief': 'solid',
                'width': 15,
                'anchor': 'n',
                'background': '#70a7cc',
                'foreground': 'black'
            }).grid(**{
                'row': 0,
                'column': i,
                'padx': 5,
                'pady': 5,
                'sticky': 'ew'
            })

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