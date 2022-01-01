import sys, time, os, subprocess
from dataio import data, crypt

def run():
    config = data.readConfigFile()
    startTimeOffset, endTimeOffset = config['startTimeOffset'], config['endTimeOffset']

    allMeetings = data.readDataFile()[1]

    if len(allMeetings) == 0:
        runGUI()
        return

    currentMeetings = [m for m in allMeetings if m.check(startTimeOffset, endTimeOffset)]

    if len(currentMeetings) == 0:
        print('There are no meetings at the moment!')
        time.sleep(5)
    elif len(currentMeetings) == 1:
        currentMeetings[0].open()
    else:
        print('There are multiple meetings at the moment.')

        for i, m in enumerate(currentMeetings):
            print(f'{i + 1:2}. {m.name:10} - {m.time if not m.isFree else "Free"}')
        
        while True:
            meetingIndex = input('Choice (0 for cancel): ')
            
            if not meetingIndex.isnumeric():
                continue

            meetingIndex = int(meetingIndex)

            if meetingIndex < 0 or meetingIndex > len(currentMeetings):
                continue

            if meetingIndex == 0:
                break

            currentMeetings[meetingIndex - 1].open()

def runGUI():
    subprocess.Popen(['pythonw', f'{sys.path[0]}/interface.pyw'])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run()
    elif sys.argv[1] in ['-c', '--config']:
        runGUI()
    elif sys.argv[1] in ['-e', '--encrypt'] and len(sys.argv) == 3:
        crypt.encrypt(sys.argv[2])
    elif sys.argv[1] in ['-d', '--decrypt'] and len(sys.argv) == 3:
        crypt.decrypt(sys.argv[2])