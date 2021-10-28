import tkinter, data

class SettingsWindow():

    def __init__(self):
        self.root = tkinter.Toplevel(background='white')
        self.root.title('Settings')

        self.setup()
        self.insert()

        self.root.mainloop()

    def setup(self):

        tkinter.Label(self.root, text='Start Time Offset (in minutes):', bg='white', padx=10, pady=10).grid()
        tkinter.Label(self.root, text='End Time Offset (in minutes):', bg='white', padx=10, pady=10).grid(row=1)
        tkinter.Label(self.root, text='Auto Delete', bg='white', padx=10, pady=10).grid(row=2)

        tkinter.Button(self.root, text='Save', command=lambda: self.save()).grid(row=3, columnspan=2)

        self.startTimeOffsetValue = tkinter.IntVar()
        self.endTimeOffsetValue = tkinter.IntVar()
        self.autoDeleteValue = tkinter.BooleanVar()

        tkinter.Entry(self.root, textvariable=self.startTimeOffsetValue).grid(row=0, column=1)
        tkinter.Entry(self.root, textvariable=self.endTimeOffsetValue).grid(row=1, column=1)
        tkinter.Checkbutton(self.root, variable=self.autoDeleteValue, bg='white').grid(row=2, column=1)

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
