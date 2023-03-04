from tkinter import ttk
import tkinter, updater
from dataio import data


class Settings(ttk.Frame):
    def __init__(self, master, config: dict):

        super().__init__(master)

        self.config = config

        self.startTimeOffset = tkinter.IntVar()
        self.endTimeOffset = tkinter.IntVar()
        self.autoDelete = tkinter.BooleanVar()
        self.hideTerminal = tkinter.BooleanVar()
        self.autoUpdate = tkinter.StringVar()
        self.openFreeMeetings = tkinter.BooleanVar()

        self.setValues()

        self.initSettings()

        column, row = self.grid_size()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.rowconfigure(row, weight=1)
        self.columnconfigure(column, weight=1)

    def initSettings(self):

        ttk.Button(self, text="<", padding=5, command=self.master.showMainMenu).grid(
            row=1, column=1, padx=5, pady=5, sticky="nw"
        )
        ttk.Button(self, text="Save", padding=5, command=self.save).grid(row=7, column=6, padx=5, pady=5, sticky="swe")

        ttk.Label(self, text="Start Time Offset", anchor="e", padding=5).grid(
            row=2, column=2, padx=5, pady=5, sticky="we"
        )
        ttk.Entry(self, textvariable=self.startTimeOffset).grid(row=2, column=3, padx=5, pady=5, sticky="we")

        ttk.Label(self, text="End Time Offset", anchor="e", padding=5).grid(
            row=3, column=2, padx=5, pady=5, sticky="we"
        )
        ttk.Entry(self, textvariable=self.endTimeOffset).grid(row=3, column=3, padx=5, pady=5, sticky="we")

        ttk.Label(self, text="Auto Delete", anchor="e", padding=5).grid(row=4, column=2, padx=5, pady=5, sticky="we")
        ttk.Checkbutton(self, variable=self.autoDelete).grid(row=4, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(self, text="Hide Terminal", anchor="e", padding=5).grid(row=5, column=2, padx=5, pady=5, sticky="we")
        ttk.Checkbutton(self, variable=self.hideTerminal, text="(Restart is required!)").grid(
            row=5, column=3, padx=5, pady=5, sticky="w"
        )

        ttk.Label(self, text="Check For Updates", anchor="e", padding=5).grid(
            row=2, column=4, padx=5, pady=5, sticky="we"
        )
        ttk.Combobox(
            self, textvariable=self.autoUpdate, state="readonly", values=["Never", "Everytime", "Daily"], width=13
        ).grid(row=2, column=5, padx=5, pady=5, sticky="we")

        ttk.Label(self, text="Open Free Meetings", anchor="e", padding=5).grid(
            row=3, column=4, padx=5, pady=5, sticky="we"
        )
        ttk.Checkbutton(self, variable=self.openFreeMeetings).grid(row=3, column=5, padx=5, pady=5, sticky="w")

        ttk.Button(self, text="Check For Updates", padding=5, command=self.checkForUpdate).grid(
            row=6, column=6, padx=5, pady=5, sticky="swe"
        )

    def setValues(self):

        self.startTimeOffset.set(self.config["startTimeOffset"])
        self.endTimeOffset.set(self.config["endTimeOffset"])
        self.autoDelete.set(self.config["autoDelete"])
        self.hideTerminal.set(self.config["hideTerminal"])
        self.autoUpdate.set(self.config["autoUpdate"])
        self.openFreeMeetings.set(self.config["openFreeMeetings"])

    def getValues(self):
        return {
            "startTimeOffset": self.startTimeOffset.get(),
            "endTimeOffset": self.endTimeOffset.get(),
            "autoDelete": self.autoDelete.get(),
            "hideTerminal": self.hideTerminal.get(),
            "autoUpdate": self.autoUpdate.get(),
            "openFreeMeetings": self.openFreeMeetings.get(),
        }

    def save(self):
        saved = ttk.Label(self, text="Saved!", padding=5, anchor="e", foreground="red")
        saved.grid(row=7, column=1, columnspan=5, padx=5, pady=5, sticky="e")

        self.config.update(**self.getValues())
        data.saveConfigFile(self.config)

        self.after(2000, saved.destroy)

    def checkForUpdate(self):

        localVersion = updater.getLocalVersion()
        remoteVersion = updater.getRemoteVersion()

        if localVersion >= remoteVersion:
            label = ttk.Label(self, text="You are using the latest version.", foreground="red", padding=5, anchor="e")
            label.grid(row=6, column=1, columnspan=5, padx=5, pady=5, sticky="e")

            self.after(5000, label.destroy)
        else:
            label = ttk.Label(
                self,
                text="New version is available. It will be installed on the next run.",
                foreground="red",
                padding=5,
                anchor="e",
            )
            label.grid(row=6, column=1, columnspan=5, padx=5, pady=5, sticky="e")

            self.config["forceUpdate"] = True
            data.saveConfigFile(self.config)

            self.after(5000, label.destroy)
