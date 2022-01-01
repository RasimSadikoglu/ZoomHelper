import os, sys, json
from itertools import cycle

def encrypt(password: str):
    with open(f'{sys.path[0]}/../files/data.json', 'r') as input:
        data = input.read()

    data = bytes(data, 'utf-8')

    password = bytes(password, 'utf-8')

    data = bytes([(int(d) + int(p)) % 256 for p, d in zip(cycle(password), data)])

    with open('files/cdata', 'wb') as out:
        out.write(data)

    print('Encryption is successful!')

def decrypt(password: str):
    if not os.path.exists(f'{sys.path[0]}/../files/cdata'):
        return

    if os.path.exists(f'{sys.path[0]}/../files/data.json'):
        cont = input('Data file will be overwritten if operation is succesful. Do you want to continue (y/n): ')
        if cont not in ['y', 'Y']:
            return  
    
    with open(f'{sys.path[0]}/../files/cdata', 'rb') as inputFile:
        data = inputFile.read()
    
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