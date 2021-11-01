import tkinter
from tkinter import font, ttk

class ConflictWindow():

    def __init__(self, meetings, config):
        self.meetings = meetings

        self.config = config

        self.root = tkinter.Tk()
        self.root.title('ZoomHelper')

        self.mainFrame = ttk.Frame(self.root)
        self.mainFrame.pack()

        self.setup()

        self.root.mainloop()

    def setup(self):
        ttk.Label(self.mainFrame, text=f'There are {len(self.meetings)} meetings at the same time.', font=font.Font(size=12)).pack(side='top')

        scrollBar = ttk.Scrollbar(self.mainFrame)
        scrollBar.pack(side='right', fill='y')

        listBox = tkinter.Listbox(self.mainFrame, selectmode='single', yscrollcommand=scrollBar.set)
        listBox.pack(fill='x')

        for i in range(len(self.meetings)):
            listBox.insert(i, self.meetings[i].info())

        ttk.Button(self.mainFrame, text='Open', command=lambda: self.open(listBox.curselection())).pack(side='left')
        ttk.Button(self.mainFrame, text='Quit', command=self.root.destroy).pack(side='right')

    def open(self, index):
        if len(index) == 0:
            return
        
        self.meetings[0].copyURL(self.root)

        self.root.after(1000, lambda: self.meetings[0].open(self.root))