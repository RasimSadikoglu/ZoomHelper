from tkinter import Tk
from frames.mainmenu import MainMenu
from frames.meetinginfo import MeetingInfo
import data
from meeting import Meeting

class Interface(Tk):

    def __init__(self):
        super().__init__()
        # self.geometry('800x325')

        self.title('ZoomHelper')
        self.protocol('WM_DELETE_WINDOW', lambda: self.check())

        (self.jsonData, self.meetings) = data.readDataFile()
        self.config = data.readConfigFile()

        self.mainMenu = MainMenu(self, self.meetings, self.jsonData)
        self.mainMenu.grid(row=0, column=0, sticky='news')

        self.currentFrame = self.mainMenu

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def check(self):
        self.destroy()

    def showMainMenu(self):
        if self.currentFrame == self.mainMenu:
            return

        self.currentFrame.destroy()

        self.mainMenu.schedule.update()
        self.mainMenu.grid()
        self.currentFrame = self.mainMenu
        
    def meetingInfo(self, meeting: Meeting):
        self.currentFrame.grid_remove()

        self.currentFrame = MeetingInfo(self, meeting)
        self.currentFrame.grid(row=0, column=0, sticky='news')