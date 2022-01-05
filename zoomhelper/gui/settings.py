from tkinter import ttk
import tkinter
from dataio import data

class Settings(ttk.Frame):

    def __init__(self, master, config: dict):

        super().__init__(master)

        self.config = config

        self.startTimeOffset = tkinter.IntVar()
        self.endTimeOffset = tkinter.IntVar()
        self.autoDelete = tkinter.BooleanVar()
        self.hideTerminal = tkinter.BooleanVar()

        self.setValues()

        self.initSettings()

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(6, weight=1)
        self.columnconfigure(4, weight=1)

    def initSettings(self):

        ttk.Button(self, text='<', padding=5, command=self.master.showMainMenu).grid(row=0, column=0, padx=5, pady=5, sticky='nw')
        ttk.Button(self, text='Save', padding=5, command=self.save).grid(row=7, column=5, padx=5, pady=5, sticky='se')

        ttk.Label(self, text='Start Time Offset', anchor='e', padding=5).grid(row=2, column=2, padx=5, pady=5, sticky='we')
        ttk.Entry(self, textvariable=self.startTimeOffset).grid(row=2, column=3, padx=5, pady=5, sticky='we')

        ttk.Label(self, text='End Time Offset', anchor='e', padding=5).grid(row=3, column=2, padx=5, pady=5, sticky='we')
        ttk.Entry(self, textvariable=self.endTimeOffset).grid(row=3, column=3, padx=5, pady=5, sticky='we')

        ttk.Label(self, text='Auto Delete', anchor='e', padding=5).grid(row=4, column=2, padx=5, pady=5, sticky='we')
        ttk.Checkbutton(self, variable=self.autoDelete).grid(row=4, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(self, text='Hide Terminal', anchor='e', padding=5).grid(row=5, column=2, padx=5, pady=5, sticky='we')
        ttk.Checkbutton(self, variable=self.hideTerminal, text='(Restart is required!)').grid(row=5, column=3, padx=5, pady=5, sticky='w')

    def setValues(self):

        self.startTimeOffset.set(self.config['startTimeOffset'])
        self.endTimeOffset.set(self.config['endTimeOffset'])
        self.autoDelete.set(self.config['autoDelete'])
        self.hideTerminal.set(self.config['hideTerminal'])

    def getValues(self):
        return {
            'startTimeOffset': self.startTimeOffset.get(),
            'endTimeOffset': self.endTimeOffset.get(),
            'autoDelete': self.autoDelete.get(),
            'hideTerminal': self.hideTerminal.get()
        }

    def save(self):
        saved = ttk.Label(self, text='Saved!', padding=5, anchor='e', foreground='red')
        saved.grid(row=7, column=4, padx=5, pady=5, sticky='e')

        self.config.update(**self.getValues())
        data.saveConfigFile(self.config)

        self.after(2000, saved.destroy)