import data, sys, time, itertools, os, json
from interface import Interface

def decrypt():
    if not os.path.exists(f'{sys.path[0]}/../files/cdata') or os.path.exists(f'{sys.path[0]}/../files/data.json'):
        return
    
    with open(f'{sys.path[0]}/../files/cdata', 'rb') as inputF:
        data = inputF.read()
    inputF.close()

    password = input('Encryted data file found please enter the password: ')
    
    password = bytes(password, 'utf-8')

    data = bytes([(int(d) - int(p) + 256) % 256 for p, d in zip(itertools.cycle(password), data)])

    try:
        data = data.decode()
        json.dumps(data)

        with open(f'{sys.path[0]}/../files/data.json', 'w') as out:
            out.write(data)
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except:
        print('Wrong password!')
    else:
        print('Data file decrypted!')
    finally:
        os.remove(f'{sys.path[0]}/../files/cdata')

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
    gui = Interface()
    gui.mainloop()

if __name__ == '__main__':
    decrypt()

    if len(sys.argv) == 1:
        run()
    elif sys.argv[1] in ['-c', '--config']:
        runGUI()