import tkinter
from tkinter import ttk

class OtherMeetingsWindow():
    def __init__(self, interface):
        self.interface = interface
        self.meetings = self.interface.otherMeetings

        self.root = tkinter.Toplevel()
        self.root.title('Other Meetings')

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close())

        self.interface.otherMeetingsWindow = True

        self.setup()

        self.root.mainloop()

    def setup(self):

        self.mainFrame = ttk.Frame(self.root)
        self.mainFrame.pack()

        scrollBar = ttk.Scrollbar(self.mainFrame)
        scrollBar.pack(side='right', fill='y')

        self.meetingsVar = tkinter.StringVar(value=self.meetings)
        listBox = tkinter.Listbox(self.mainFrame, listvariable=self.meetingsVar, selectmode='single', width=40, yscrollcommand=scrollBar.set)
        listBox.pack(fill='x')

        ttk.Button(self.mainFrame, text='Edit', command=lambda: self.update(listBox.curselection(), 'EDIT')).pack(side='left')
        ttk.Button(self.mainFrame, text='Delete', command=lambda: self.update(listBox.curselection(), 'DELETE')).pack(side='right')

    def update(self, index=[], op='UPDATE'):

        if (len(index) == 0 or self.interface.isTherePopUp) and op != 'UPDATE':
            return

        if op == 'DELETE':
            self.meetings[index[0]].markForDelete = True
            self.meetings.remove(self.meetings[index[0]])
        elif op == 'EDIT':
            self.interface.meetingInfo(self.interface.meetings.index(self.meetings[index[0]]), self.interface.calendarFrame, self)
            
        self.meetingsVar.set(self.meetings)

    def close(self):
        self.root.destroy()
        self.interface.otherMeetingsWindow = False
