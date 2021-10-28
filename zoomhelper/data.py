import json
import sys
import meeting

def readDataFile():
    try:
        with open(f'{sys.path[0]}/data.json', "r") as dataFile:
            jsonData = json.load(dataFile)
    except:
        print('No JSON file found!')
        return ([], [])

    meetings = []

    for i in range(len(jsonData)):
        meetings.append(meeting.Meeting.jsonDeserialize(jsonData[i]))

    return (jsonData, meetings)

def saveDataFile(meetings):

    jsonData = []

    for i in range(len(meetings)):

        if meetings[i].markForDelete:
            continue

        jsonData.append(meetings[i].jsonSerialize())

    with open(f'{sys.path[0]}/data.json', "w") as dataFile:
        json.dump(jsonData, dataFile, indent=4)


def readConfigFile():
    try:
        with open(f'{sys.path[0]}/config.json', "r") as configFile:
            return json.load(configFile)
    except:
        print("Error no config file is found!")
        exit

def saveConfigFile(config):

    with open(f'{sys.path[0]}/config.json', "w") as configFile:
        json.dump(config, configFile, indent=4)