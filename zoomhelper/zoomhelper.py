import data, sys, time, itertools, os
from interface import Interface

def decrypt():
    if not os.path.exists(f'{sys.path[0]}/../files/cdata') or os.path.exists(f'{sys.path[0]}/../files/data.json'):
        return
    
    try:
        with open(f'{sys.path[0]}/../files/cdata', 'rb') as inputF:
            data = inputF.read()
        inputF.close()

        password = input('Encryted data file found please enter the password: ')
        
        password = bytes(password, 'utf-8')

        data = bytes([(int(d) - int(p) + 256) % 256 for p, d in zip(itertools.cycle(password), data)])

        with open(f'{sys.path[0]}/../files/data.json', 'w') as out:
            out.write(data.decode())
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except:
        os.remove(f'{sys.path[0]}/../files/data.json')
        print('Wrong password!')
    else:
        print('Data file decrypted!')

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
    decrypt()

    if len(sys.argv) == 1:
        run()
    elif sys.argv[1] == '-c' or sys.argv[1] == '--config':
        gui = Interface()
        gui.mainloop()