# import data, tkinter, datetime, re
# from frames.settings_window import SettingsWindow
# from frames.dateframe import DateFrame
# from frames.other_meetings_window import OtherMeetingsWindow
# from tkinter.font import Font

from tkinter import Tk
from frames.mainmenu import MainMenu
import data

class Interface(Tk):

    def __init__(self):
        super().__init__()

        self.title('ZoomHelper')
        self.protocol('WM_DELETE_WINDOW', lambda: self.check())

        (self.jsonData, self.meetings) = data.readDataFile()
        self.config = data.readConfigFile()

        self.meetings = sorted(self.meetings, key=lambda x: (x.date.weekday() if x.date != None else x.weekDay, x.time))

        self.mainMenu = MainMenu(self, self.meetings)
        self.mainMenu.grid(sticky='news')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def check(self):
        self.destroy()
        
    # def setCalendarFrame(self):

    #     self.calendarFrame = ttk.Frame(self.master)
    #     self.calendarFrame.grid()
        
    #     maxRows = self.getMeetingsInGroup(self.calendarFrame) - 1

    #     def changeDateWindow(direction):
    #         if self.otherMeetingsWindow:
    #             return
    #         if direction != 0:
    #             (self.startDate, self.endDate) = (self.startDate + datetime.timedelta(days=direction), self.endDate + datetime.timedelta(days=direction))
    #         else:
    #             (self.startDate, self.endDate) = (self.dateOfToday - datetime.timedelta(days=self.dateOfToday.weekday()), self.dateOfToday + datetime.timedelta(days=6-self.dateOfToday.weekday()))

    #         self.calendarFrame.destroy()
    #         self.setCalendarFrame()

    #     ttk.Button(self.calendarFrame, text="<", command=lambda: changeDateWindow(-7)).grid(row=0, column=0)
    #     ttk.Button(self.calendarFrame, text=">", command=lambda: changeDateWindow(7)).grid(row=0, column=6)

    #     dateLabel = ttk.Label(self.calendarFrame, text=datetime.datetime.today().strftime('%d %B, %Y - %A'), cursor="hand2")
    #     dateLabel.grid(row=0, column=1, columnspan=5)
    #     dateLabel.bind('<Button-1>', lambda e: changeDateWindow(0))

    #     ttk.Button(self.calendarFrame, text="Settings", command=lambda: SettingsWindow()).grid(row=0, column=7)

    #     dateOfWeekday = self.startDate
    #     for i in range(7):
    #         stringDate = f'{meeting.weekDays[i]}\n{dateOfWeekday.strftime("%d/%m/%y")}'
    #         ttk.Label(self.calendarFrame, text=stringDate, background=('white', '#69E7FF')[dateOfWeekday == self.dateOfToday]).grid(row=1, column=i)
    #         dateOfWeekday += datetime.timedelta(days=1)

    #     maxRows = max(maxRows, 4)

    #     ttk.Button(self.calendarFrame, text="Other Meetings", command=lambda: OtherMeetingsWindow(self)).grid(row=maxRows + 1, column=0)

    #     ttk.Label(self.calendarFrame, text="Left Click for Edit - Right Click for Delete").grid(row=maxRows + 2, column=0, columnspan=8)

    #     def saveMeetings():
    #         if self.isTherePopUp or self.otherMeetingsWindow:
    #             return
            
    #         data.saveDataFile(self.meetings)
    #         (self.jsonData, self.meetings) = data.readDataFile()
    #         self.calendarFrame.destroy()
    #         self.setCalendarFrame()

    #     ttk.Button(self.calendarFrame, text="Save", command=saveMeetings).grid(row=maxRows, column=7)

    #     def revertMeetings():
    #         if self.isTherePopUp or self.otherMeetingsWindow:
    #             return

    #         self.meetings = [meeting.Meeting.jsonDeserialize(m) for m in self.jsonData]
    #         self.calendarFrame.destroy()
    #         self.setCalendarFrame()

    #     ttk.Button(self.calendarFrame, text="Revert", command=revertMeetings).grid(row=maxRows - 1, column=7)

    #     ttk.Button(self.calendarFrame, text="Add", command=lambda: self.meetingInfo(-1, self.calendarFrame)).grid(row=maxRows - 2, column=7)

    #     for child in self.calendarFrame.winfo_children(): 
    #         child.grid_configure(padx=5, pady=5)

    # def getMeetingsInGroup(self, frame):

    #     self.otherMeetings.clear()
    #     meetingsInGroup = [[], [], [], [], [], [], []]

    #     for m in self.meetings:
    #         if m.isFree:
    #             self.otherMeetings.append(m)
    #         elif m.weekDay != -1:
    #             meetingsInGroup[m.weekDay].append(m)
    #         elif m.startDate >= self.startDate and m.startDate <= self.endDate:
    #             meetingsInGroup[m.startDate.weekday()].append(m)
    #         else:
    #             self.otherMeetings.append(m)

    #     meetingsInGroup = [sorted(m, key=lambda mt: [mt.startDate.hour, mt.startDate.minute]) for m in meetingsInGroup]

    #     def deleteMeeting(index):
    #         self.meetings[index].markForDelete = not self.meetings[index].markForDelete
    #         frame.destroy()
    #         self.setCalendarFrame()

    #     def meetingColor(m):
    #         if m.markForDelete:
    #             return "#FF5A40"
    #         else:
    #             return ("#E8FF89", "white")[m.jsonSerialize() in self.jsonData]

    #     meetingsIndex = [2 for i in range(7)]

    #     for i in range(7):
    #         for m in meetingsInGroup[i]:
    #             meetingLabel = ttk.Label(frame, text=m.labelInfo(), cursor="hand2", background=meetingColor(m))
    #             meetingLabel.grid(row=meetingsIndex[i], column=i)

    #             meetingLabel.bind("<Button-1>", lambda e, index=self.meetings.index(m): self.meetingInfo(index, frame))
    #             meetingLabel.bind("<Button-3>", lambda e, index=self.meetings.index(m): deleteMeeting(index))

    #             meetingsIndex[i] += 1

    #     return max(meetingsIndex)

    # def meetingInfo(self, index, frame, otherMeetings=None):
    #     if self.isTherePopUp:
    #         return

    #     self.isTherePopUp = True

    #     meetingInfoWindow = tkinter.Toplevel()
    #     meetingInfoWindow.title("Add New Meeting" if index == -1 else "Meeting Info")

    #     def closeMeetingInfoWindow(op):
    #         if op == 1:
    #             mt = {
    #                 "name": "",
    #                 "id": "",
    #                 "password": "",
    #                 "startDate": {
    #                 "year": 2022,
    #                 "month": 1,
    #                 "day": 1,
    #                 "hour": 0,
    #                 "minute": 0
    #                 },
    #                 "endDate": {
    #                 "year": 2022,
    #                 "month": 1,
    #                 "day": 1,
    #                 "hour": 0,
    #                 "minute": 0
    #                 },
    #                 "weekDay": -1,
    #                 "isFree": False,
    #                 "platform": "Zoom"
    #             }

    #             mt['name'] = self.meetingNameEntry.get()
    #             mt['id'] = self.idEntry.get()
    #             mt['password'] = self.passwordEntry.get()

    #             if self.dateFrame.isFree:
    #                 mt['isFree'] = True

    #             elif self.dateFrame.repetitive.get():
    #                 mt['weekDay'] = meeting.weekDays.index(self.dateFrame.weekDayVar.get())

    #                 mt['startDate']['hour'] = int(self.dateFrame.startDateEntries[3].get())
    #                 mt['startDate']['minute'] = int(self.dateFrame.startDateEntries[4].get())

    #                 mt['endDate']['hour'] = int(self.dateFrame.endDateEntries[3].get())
    #                 mt['endDate']['minute'] = int(self.dateFrame.endDateEntries[4].get())

    #             else:
    #                 mt['startDate']['year'] = int(self.dateFrame.startDateEntries[0].get())
    #                 mt['startDate']['month'] = int(self.dateFrame.startDateEntries[1].get())
    #                 mt['startDate']['day'] = int(self.dateFrame.startDateEntries[2].get())
    #                 mt['startDate']['hour'] = int(self.dateFrame.startDateEntries[3].get())
    #                 mt['startDate']['minute'] = int(self.dateFrame.startDateEntries[4].get())

    #                 mt['endDate']['hour'] = int(self.dateFrame.endDateEntries[3].get())
    #                 mt['endDate']['minute'] = int(self.dateFrame.endDateEntries[4].get())

    #                 if self.dateFrame.differentEndTime.get():
    #                     mt['endDate']['year'] = int(self.dateFrame.endDateEntries[0].get())
    #                     mt['endDate']['month'] = int(self.dateFrame.endDateEntries[1].get())
    #                     mt['endDate']['day'] = int(self.dateFrame.endDateEntries[2].get())
    #                 else:
    #                     mt['endDate']['year'] = int(self.dateFrame.startDateEntries[0].get())
    #                     mt['endDate']['month'] = int(self.dateFrame.startDateEntries[1].get())
    #                     mt['endDate']['day'] = int(self.dateFrame.startDateEntries[2].get())
                    

    #             if index != -1:
    #                 self.meetings[index] = Meeting.jsonDeserialize(mt)
    #             else:
    #                 self.meetings.append(Meeting.jsonDeserialize(mt))
                
    #         elif op == 2 and index != -1:
    #             self.meetings[index].markForDelete = True

    #         meetingInfoWindow.destroy()
    #         frame.destroy()
    #         self.setCalendarFrame()
    #         if otherMeetings != None:
    #             otherMeetings.update()

    #         self.isTherePopUp = False

    #     meetingInfoWindow.protocol("WM_DELETE_WINDOW", lambda: closeMeetingInfoWindow(0))

    #     infoFrame = ttk.Frame(meetingInfoWindow)
    #     infoFrame.grid(row=0)

    #     def parseLink():
    #         text = linkEntry.get()

    #         id = re.findall('zoom.us/[jw]/(\d+)', text)
    #         password = re.findall('pwd=(\w+)', text)

    #         if len(id) != 1 or len(password) != 1:
    #             return

    #         self.idEntry.delete(0, tkinter.END)
    #         self.idEntry.insert(0, id[0])

    #         self.passwordEntry.delete(0, tkinter.END)
    #         self.passwordEntry.insert(0, password[0])

    #     # Row 0
    #     ttk.Label(infoFrame, text="Link:", width=16, anchor='e').grid(row=0, column=0, columnspan=2)

    #     linkEntry = tkinter.Entry(infoFrame, width=24)
    #     linkEntry.grid(row=0, column=2, columnspan=3, pady=10, padx=5)

    #     ttk.Button(infoFrame, text='Parse', command=parseLink).grid(row=0, column=5)

    #     # Row 1
    #     ttk.Label(infoFrame, text='Meeting Name:', width=16, anchor='e').grid(row=1, column=0, columnspan=2)

    #     self.meetingNameEntry = tkinter.Entry(infoFrame, width=24)
    #     self.meetingNameEntry.grid(row=1, column=2, columnspan=3, pady=10, padx=5)

    #     # Row 2
    #     ttk.Label(infoFrame, text='ID:', width=16, anchor='e').grid(row=2, column=0, columnspan=2)

    #     self.idEntry = tkinter.Entry(infoFrame, width=24)
    #     self.idEntry.grid(row=2, column=2, columnspan=3, pady=10, padx=5)

    #     # Row 3
    #     ttk.Label(infoFrame, text='Password:', width=16, anchor='e').grid(row=3, column=0, columnspan=2)

    #     self.passwordEntry = tkinter.Entry(infoFrame, width=24)
    #     self.passwordEntry.grid(row=3, column=2, columnspan=3, pady=10, padx=5)

    #     if index != -1:
    #         self.meetingNameEntry.insert(0, self.meetings[index].name)
    #         self.idEntry.insert(0, self.meetings[index].id)
    #         self.passwordEntry.insert(0, self.meetings[index].password)

    #     args: dict

    #     if index == -1:
    #         args = {
    #             'mt': None
    #         }
    #     else:
    #         args = {
    #             'mt': self.meetings[index],
    #             'det': self.meetings[index].weekDay == -1,
    #             'r': self.meetings[index].weekDay != -1,
    #             'isFree': self.meetings[index].isFree
    #         }

    #     self.dateFrame = DateFrame(meetingInfoWindow, **args)

    #     buttonFrame = ttk.Frame(meetingInfoWindow)
    #     buttonFrame.grid(row=2)

    #     ttk.Button(buttonFrame, text=('Add', 'Update')[index != -1], command=lambda: closeMeetingInfoWindow(1)).grid(row=1, column=0, columnspan=2)
    #     ttk.Button(buttonFrame, text=('Exit', 'Delete')[index != -1], command=lambda: closeMeetingInfoWindow(2)).grid(row=1, column=4, columnspan=2)

    #     isFree = tkinter.BooleanVar()
    #     isFree.set(self.dateFrame.isFree)
    #     ttk.Checkbutton(buttonFrame, text='Free', variable=isFree,command=lambda: self.dateFrame.reset(isFree.get())).grid(row=1, column=2, columnspan=2, pady=10, padx=10)

    #     meetingInfoWindow.transient(self.master)
    #     meetingInfoWindow.wait_visibility()
    #     meetingInfoWindow.grab_set()
    #     meetingInfoWindow.wait_window()

    # def check(self):

    #     meetingsLength = 0
    #     for m in self.meetings:
    #         meetingsLength += not m.markForDelete
        
    #     changes = False

    #     if meetingsLength != len(self.jsonData):
    #         changes = True

    #     for m in self.meetings:
    #         if changes:
    #             break
    #         if not m.markForDelete and m.jsonSerialize() not in self.jsonData:
    #             changes = True

    #     if changes:
    #         self.changeWarning()
    #     else:
    #         self.master.destroy()

    # def changeWarning(self):

    #     changeWarningWindow = tkinter.Toplevel()
    #     changeWarningWindow.title('Discard Changes')

    #     ttk.Label(changeWarningWindow, text='Your changes have not been saved!', font=Font(size=12)).grid(columnspan=2)

    #     ttk.Button(changeWarningWindow, text='Quit Anyway', command=self.master.destroy).grid(row=1)

    #     def save():
    #         data.saveDataFile(self.meetings)
    #         self.master.destroy()

    #     ttk.Button(changeWarningWindow, text='Save', command=save).grid(row=1, column=1)

    #     changeWarningWindow.transient(self.master)
    #     changeWarningWindow.wait_visibility()
    #     changeWarningWindow.grab_set()
    #     changeWarningWindow.wait_window()