import os, sys, json
from itertools import cycle

def encrypt():
    with open('files/data.json', 'r') as input:
        data = input.read()

    data = bytes(data, 'utf-8')

    password = bytes('helperzoom', 'utf-8')

    data = bytes([(int(d) + int(p)) % 256 for p, d in zip(cycle(password), data)])

    with open('files/cdata', 'wb') as out:
        out.write(data)

def decrypt(password: str):
    with open('files/cdata', 'rb') as input:
        data = input.read()

    password = bytes(password, 'utf-8')

    data = bytes([(int(d) - int(p) + 256) % 256 for p, d in zip(cycle(password), data)])

    print(data.decode('utf-8'))

def decrypt():
    if not os.path.exists(f'{sys.path[0]}/../files/cdata') or os.path.exists(f'{sys.path[0]}/../files/data.json'):
        return
    
    with open(f'{sys.path[0]}/../files/cdata', 'rb') as inputF:
        data = inputF.read()
    inputF.close()

    password = input('Encryted data file found please enter the password: ')
    
    password = bytes(password, 'utf-8')

    data = bytes([(int(d) - int(p) + 256) % 256 for p, d in zip(cycle(password), data)])

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