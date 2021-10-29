import tkinter, data
from tkinter import ttk

class SettingsWindow():

    def __init__(self):
        self.root = tkinter.Toplevel()
        self.root.title('Settings')

        self.frame = ttk.Frame(self.root)
        self.frame.grid()

        self.setup()
        self.insert()

        self.root.mainloop()

    def setup(self):

        ttk.Label(self.frame, text='Start Time Offset (in minutes):').grid()
        ttk.Label(self.frame, text='End Time Offset (in minutes):').grid(row=1)
        ttk.Label(self.frame, text='Auto Delete').grid(row=2)

        ttk.Button(self.frame, text='Save', command=lambda: self.save()).grid(row=3, columnspan=2)

        self.startTimeOffsetValue = tkinter.IntVar()
        self.endTimeOffsetValue = tkinter.IntVar()
        self.autoDeleteValue = tkinter.BooleanVar()

        ttk.Entry(self.frame, textvariable=self.startTimeOffsetValue).grid(row=0, column=1)
        ttk.Entry(self.frame, textvariable=self.endTimeOffsetValue).grid(row=1, column=1)
        ttk.Checkbutton(self.frame, variable=self.autoDeleteValue).grid(row=2, column=1)

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def insert(self):

        config = data.readConfigFile()

        self.startTimeOffsetValue.set(config['startTimeOffset'])
        self.endTimeOffsetValue.set(config['endTimeOffset'])
        self.autoDeleteValue.set(config['autoDelete'])

    def save(self):

        config = {
            'startTimeOffset': self.startTimeOffsetValue.get(),
            'endTimeOffset': self.endTimeOffsetValue.get(),
            'autoDelete': self.autoDeleteValue.get()
        }

        data.saveConfigFile(config)

        self.root.destroy()
