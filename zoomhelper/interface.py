from tkinter import Tk
from gui.mainmenu import MainMenu
from gui.meetinginfo import MeetingInfo
from meeting.meeting import Meeting
from dataio import data
import atexit

class Interface(Tk):

    def __init__(self, meetings: list[Meeting], jsonData: list[dict], config: dict):
        super().__init__()

        self.title('ZoomHelper')
        self.protocol('WM_DELETE_WINDOW', lambda: self.exitCheck())

        (self.jsonData, self.meetings) = jsonData, meetings
        self.config = config

        atexit.register(data.saveDataFile, meetings)

        self.mainMenu = MainMenu(self, self.meetings, self.jsonData)
        self.mainMenu.grid(row=0, column=0, sticky='news')

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
        self.geometry(self.winfo_geometry())
        self.update()

        self.currentFrame.grid_remove()

        self.currentFrame = MeetingInfo(self, meeting)
        self.currentFrame.grid(row=0, column=0, sticky='news')

def main(meetings: list[Meeting], jsonData: list[dict], config: dict):
    gui = Interface(meetings, jsonData, config)
    gui.mainloop()

if __name__ == '__main__':
    jsonData, meetings = data.readDataFile()
    config = data.readConfigFile()

    main(meetings, jsonData, config)