import interface, data, sys, datetime, tkinter, conflict_window
from tkinter import messagebox

def run():
    config = data.readConfigFile()

    meetings = data.readDataFile()[1]

    save = len(meetings) > 0

    now = datetime.datetime.today()

    currentMeetings = []

    for m in meetings:

        if m.isFree:
            currentMeetings.append(m)

        elif m.weekDay == -1:
            sd = m.startDate
            ed = m.endDate

            sd += datetime.timedelta(minutes=config['startTimeOffset'])
            ed += datetime.timedelta(minutes=config['endTimeOffset'])

            if now > sd and now < ed:
                currentMeetings.append(m)
            elif now > ed and config['autoDelete']:
                meetings.remove(m)
        elif m.weekDay == now.weekday():
            sd = m.startDate
            ed = m.endDate

            sd += datetime.timedelta(minutes=config['startTimeOffset'])
            ed += datetime.timedelta(minutes=config['endTimeOffset'])

            sd = [sd.hour, sd.minute]
            ed = [ed.hour, ed.minute]

            n = [now.hour, now.minute]

            if n > sd and n < ed:
                currentMeetings.append(m)

    if len(currentMeetings) > 2:
        conflict_window.ConflictWindow(currentMeetings, config)
    elif len(currentMeetings) == 1:
        root = tkinter.Tk()
        root.withdraw()

        currentMeetings[0].copyURL(root)

        root.after(1000, lambda: currentMeetings[0].open(root))
        
        root.mainloop()
    else:
        root = tkinter.Tk()
        root.withdraw()
        root.after(2000, root.destroy)
        messagebox.showinfo('ZoomHelper', 'There is no meeting at the moment!')

    if save:
        data.saveDataFile(meetings)

def openInterface():
    interface.Interface()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run()
    elif sys.argv[1] == '-c' or sys.argv[1] == '--config':
        openInterface()