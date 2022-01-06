import reqirements
reqirements.install()

import updater
updater.checkForUpdate()

import sys, time, subprocess, interface, os, glob
from dataio import data, crypt
from meeting.meeting import Status

class ZoomHelper:

    def __init__(self):
        self.jsonData, self.meetings = data.readDataFile()
        
        self.config = data.readConfigFile()

    def setup(self):
        if self.config['autoDelete']:
            self.autoDelete()

        if len(sys.argv) == 1:
            self.run()
        elif sys.argv[1] in ['-c', '--config']:
            self.runGUI()
        elif sys.argv[1] in ['-e', '--encrypt'] and len(sys.argv) == 3:
            crypt.encrypt(sys.argv[2])
        elif sys.argv[1] in ['-d', '--decrypt'] and len(sys.argv) == 3:
            crypt.decrypt(sys.argv[2])

    def run(self):
        startTimeOffset, endTimeOffset = self.config['startTimeOffset'], self.config['endTimeOffset']

        if len(self.meetings) == 0:
            self.runGUI()
            return

        currentMeetings = [m for m in self.meetings if m.check(startTimeOffset, endTimeOffset, self.config['openFreeMeetings']) == Status.READY]

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

    def runGUI(self):
        pythonw = False

        for p in os.getenv('PATH').split(';'):

            if len(glob.glob(p + '/pythonw*')) != 0:
                pythonw = True
                break

        if pythonw and self.config['hideTerminal']:
            subprocess.Popen(['pythonw', f'{sys.path[0]}/interface.py'])
        else:
            interface.main(self.meetings, self.jsonData, self.config)

    def autoDelete(self):
        
        meetings = [m for m in self.meetings if m.check(self.config['startTimeOffset'], self.config['endTimeOffset']) != Status.OLD]

        data.saveDataFile(meetings)

        self.jsonData, self.meetings = data.readDataFile()

if __name__ == '__main__':
    zh = ZoomHelper()
    zh.setup()