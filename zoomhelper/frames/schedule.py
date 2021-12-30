from tkinter import Tk, ttk

class Schedule(ttk.Frame):

    def __init__(self, master: Tk, meetings: list):
        super().__init__(master, padding=5)
        self.grid(sticky='news')
        ttk.Label(self, text='Hello', background='black').grid(sticky='news')

        self.meetings = meetings