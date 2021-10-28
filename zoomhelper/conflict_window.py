import tkinter
from tkinter import font

class ConflictWindow():

    def __init__(self, meetings):
        self.meetings = meetings

        self.root = tkinter.Tk()
        self.root.title('ZoomHelper')

        self.mainFrame = tkinter.Frame(self.root, bg='white')
        self.mainFrame.pack()

        self.setup()

        self.root.mainloop()

    def setup(self):
        tkinter.Label(self.mainFrame, text=f'There are {len(self.meetings)} meetings at the same time.', font=font.Font(size=12), bg='white').pack(side='top')

        scrollBar = tkinter.Scrollbar(self.mainFrame, bg='white')
        scrollBar.pack(side='right', fill='y')

        listBox = tkinter.Listbox(self.mainFrame, selectmode='single', yscrollcommand=scrollBar.set)
        listBox.pack(fill='x')

        for i in range(len(self.meetings)):
            listBox.insert(i, self.meetings[i].labelInfo())

        tkinter.Button(self.mainFrame, text='Open', command=lambda: self.open(listBox.curselection())).pack(side='left')
        tkinter.Button(self.mainFrame, text='Quit', command=self.root.destroy).pack(side='right')

    def open(self, index):
        if len(index) == 0:
            return
        
        self.meetings[index[0]].open()
        self.root.destroy()
