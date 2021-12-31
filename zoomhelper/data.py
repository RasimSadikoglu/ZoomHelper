import json, sys
from meeting import Meeting

def readDataFile(meetings: list=None) -> list[Meeting]:
    try:
        with open(f'{sys.path[0]}/../files/data.json', "r") as dataFile:
            jsonData = json.load(dataFile)
    except:
        if meetings != None:
            meetings.clear()
            return
        else:
            print('No JSON file found!')
            return ([], [])

    if meetings != None:
        meetings.clear()
    else:
        meetings = []

    for i in range(len(jsonData)):
        meetings.append(Meeting.jsonDeserialize(jsonData[i]))

    return (jsonData, meetings)

def saveDataFile(meetings: list[Meeting]) -> None:

    jsonData = []

    for i in range(len(meetings)):

        jsonData.append(meetings[i].jsonSerialize())

    with open(f'{sys.path[0]}/../files/data.json', "w") as dataFile:
        json.dump(jsonData, dataFile, indent=4)


def readConfigFile() -> dict:
    try:
        with open(f'{sys.path[0]}/../files/config.json', "r") as configFile:
            return json.load(configFile)
    except FileNotFoundError:
        raise FileNotFoundError(f'Config file is missing!\n{sys.path[0]}../files/config.json')

def saveConfigFile(config: dict):

    with open(f'{sys.path[0]}/../files/config.json', "w") as configFile:
        json.dump(config, configFile, indent=4)