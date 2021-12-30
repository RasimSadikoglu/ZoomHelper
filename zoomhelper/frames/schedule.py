from tkinter import ttk
from meeting import Meeting
from datetime import datetime, timedelta

weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class Schedule(ttk.Frame):

    def __init__(self, master: ttk.Frame, meetings: list[Meeting], timeWindow: dict):
        super().__init__(master, padding=5)

        self.meetings = meetings
        self.timeWindow = timeWindow

        self.initGrid()
        
        column, row = self.grid_size()

        for i in range(row):
            self.rowconfigure(i, weight=1)

        for i in range(column):
            self.columnconfigure(i, weight=1)

    def initGrid(self):
        grid = [[] for i in range(7)]

        for m in self.meetings:
            weekDay = m.date.weekday() if m.date != None else m.weekDay
            grid[weekDay].append(m)

        self.placeGrid(grid)

    def placeGrid(self, grid: list[list[Meeting]]):
        today = self.timeWindow['begin']

        for w, i in zip(weekDays, range(len(weekDays))):
            labelOptions = {
                'text': f'{w}\n{str(today)}',
                'padding': 5,
                'relief': 'solid',
                'anchor': 'center',
                'background': '#69E7FF' if today == datetime.now().date() else 'white'
            }

            gridOptions = {
                'row': 0,
                'column': i,
                'padx': 5,
                'pady': 5,
                'sticky': 'news'
            }

            ttk.Label(self, **labelOptions).grid(**gridOptions)

            today += timedelta(days=1)

        for day, column in zip(grid, range(len(grid))):
            for meeting, row in zip(day, range(1, len(day) + 1)):
                labelOptions = {
                    'text': str(meeting),
                    'padding': 5,
                    'relief': 'solid',
                    'anchor': 'center',
                    'background': 'white'
                }

                gridOptions = {
                    'row': row,
                    'column': column,
                    'padx': 5,
                    'pady': 5,
                    'sticky': 'news'
                }

                ttk.Label(self, **labelOptions).grid(**gridOptions)

    def update(self):
        for child in self.winfo_children():
            child.destroy()

        self.initGrid()