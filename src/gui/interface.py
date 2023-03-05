from base import reqirements

reqirements.install()

from tkinter import Tk
from gui.mainmenu import MainMenu
from gui.meetinginfo import MeetingInfo
from gui.settings import Settings
from models.meeting import Meeting
from dataio import data


class Interface(Tk):
    def __init__(self, meetings: list[Meeting], jsonData: list[dict]):
        super().__init__()

        self.title("ZoomHelper")
        self.protocol("WM_DELETE_WINDOW", lambda: self.exitCheck())
        self.bind("<MouseWheel>", lambda e: self.mouseWheelEvent(e))
        self.bind("<Button-4>", lambda e: self.mouseWheelEvent(e))
        self.bind("<Button-5>", lambda e: self.mouseWheelEvent(e))

        (self.jsonData, self.meetings) = jsonData, meetings

        self.mainMenu = MainMenu(self, self.meetings, self.jsonData)
        self.mainMenu.grid(row=0, column=0, sticky="news")

        self.currentFrame = self.mainMenu

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.update()

        self.minsize(self.winfo_width(), self.winfo_height())

    def exitCheck(self):
        self.showMainMenu()

        if self.mainMenu.exitCheck():
            self.destroy()

    def showMainMenu(self):
        if self.currentFrame == self.mainMenu:
            return

        self.currentFrame.destroy()

        self.mainMenu.schedule.update()
        self.mainMenu.grid()
        self.currentFrame = self.mainMenu

        self.geometry("")
        self.update()

    def meetingInfo(self, meeting: Meeting):
        self.geometry(max(self.winfo_geometry(), "919x415"))
        self.update()

        self.currentFrame.grid_remove()

        self.currentFrame = MeetingInfo(self, meeting)
        self.currentFrame.grid(row=0, column=0, sticky="news")

    def settings(self):
        self.geometry(max(self.winfo_geometry(), "919x415"))
        self.update()

        self.currentFrame.grid_remove()

        self.currentFrame = Settings(self)
        self.currentFrame.grid(row=0, column=0, sticky="news")

    def mouseWheelEvent(self, event):
        if self.currentFrame == self.mainMenu:
            self.mainMenu.mouseWheelEvent(event)


def main(meetings: list[Meeting], jsonData: list[dict]):
    gui = Interface(meetings, jsonData)
    gui.mainloop()


if __name__ == "__main__":
    jsonData, meetings = data.readDataFile()
    config = data.readConfigFile()

    main(meetings, jsonData)
