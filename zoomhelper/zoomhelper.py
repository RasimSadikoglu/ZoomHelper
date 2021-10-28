import interface, data, sys, datetime, tkinter, conflict_window
from tkinter import messagebox

config = data.readConfigFile()

def run():
    meetings = data.readDataFile()[1]

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
        conflict_window.ConflictWindow(currentMeetings)
    elif len(currentMeetings) == 1:
        currentMeetings[0].open()
    else:
        tkinter.Tk().withdraw()
        messagebox.showinfo('ZoomHelper', 'Currently there is no meeting!')

    data.saveDataFile(meetings)

def openInterface():
    interface.Interface()

def test():
    return

if (len(sys.argv) > 1 and (sys.argv[1] == "--config" or sys.argv[1] == "-c")):
    openInterface()
elif (len(sys.argv) > 1 and sys.argv[1] == "--test"):
    test()
else:
    run()