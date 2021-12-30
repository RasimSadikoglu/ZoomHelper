import data, sys, time
from interface import Interface

def run():

    config = data.readConfigFile()
    startTimeOffset, endTimeOffset = config['startTimeOffset'], config['endTimeOffset']

    meetings = [m for m in data.readDataFile()[1] if m.check(startTimeOffset, endTimeOffset)]

    if len(meetings) == 0:
        print('There are no meetings!')
        time.sleep(5)
    else:
        meetings[0].open()

if __name__ == '__main__':

    if len(sys.argv) == 1:
        run()
    elif sys.argv[1] == '-c' or sys.argv[1] == '--config':
        gui = Interface()
        gui.mainloop()