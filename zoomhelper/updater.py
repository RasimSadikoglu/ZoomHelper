import requests, sys, os, zipfile, shutil, datetime
from dataio import data

def update():

    config = data.readConfigFile()

    if not config['autoUpdate']:
        return

    today = datetime.datetime.now().day

    if config['lastUpdateCheck'] == today:
        return

    localVersion = getLocalVersion()
    remoteVersion = getRemoteVersion()

    if localVersion < remoteVersion:
        print('New version is found. Attempting to update.')

        download()
        extract()
        updateFiles()
        clean()

    config['lastUpdateCheck'] = today

def getLocalVersion():
    try:
        with open(f'{sys.path[0]}/../files/.version', "r") as vFile:
            return vFile.read()
    except:
        return 'v0.0.0'

def getRemoteVersion():
    versionUrl = 'https://raw.githubusercontent.com/RasimSadikoglu/ZoomHelper/release/files/.version'

    version = requests.get(versionUrl)

    return version.text

def download():
    print('(1/4) Downloading new version.')

    url = 'https://github.com/RasimSadikoglu/ZoomHelper/archive/refs/heads/release.zip'

    updatePackage = requests.get(url)

    if not os.path.exists(f'{sys.path[0]}/../.update/'):
        os.mkdir(f'{sys.path[0]}/../.update/')

    with open(f'{sys.path[0]}/../.update/update_package.zip', 'wb') as f:
        f.write(updatePackage.content)

def extract():
    print('(2/4) Extracting downloaded package.')

    with zipfile.ZipFile(f'{sys.path[0]}/../.update/update_package.zip', 'r') as updPkg:
        updPkg.extractall(f'{sys.path[0]}/../.update/')

def updateFiles():
    print('(3/4) Updating files.')

    shutil.copytree(f'{sys.path[0]}/../.update/ZoomHelper-release/files/', f'{sys.path[0]}/../files/', dirs_exist_ok=True)
    shutil.copytree(f'{sys.path[0]}/../.update/ZoomHelper-release/zoomhelper/', f'{sys.path[0]}/../zoomhelper/', dirs_exist_ok=True)

def clean():
    print('(4/4) Cleaning up.')

    shutil.rmtree(f'{sys.path[0]}/../.update/')