import subprocess, sys, time

def install():

    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', f'{sys.path[0]}/requirements.txt'])
    print('Please restart the program!')
    time.sleep(3)
    exit(0)