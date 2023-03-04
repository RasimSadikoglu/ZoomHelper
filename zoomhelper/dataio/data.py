import json, sys, os, shutil
from meeting.meeting import Meeting


def readDataFile(meetings: list = None) -> list[Meeting]:
    try:
        with open(f"{sys.path[0]}/../files/data.json", "r") as dataFile:
            jsonData = json.load(dataFile)
    except:
        if meetings != None:
            meetings.clear()
            return
        else:
            print("No JSON file found!")
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

    for m in meetings:

        jsonData.append(m.jsonSerialize())

    with open(f"{sys.path[0]}/../files/data.json", "w") as dataFile:
        json.dump(jsonData, dataFile, indent=4)


def readConfigFile() -> dict:
    if not os.path.exists(f"{sys.path[0]}/../files/config.json"):
        shutil.copy(f"{sys.path[0]}/../files/default_config.json", f"{sys.path[0]}/../files/config.json")

    try:
        config = {}

        with open(f"{sys.path[0]}/../files/default_config.json", "r") as dfc:
            config = json.load(dfc)

        with open(f"{sys.path[0]}/../files/config.json", "r") as configFile:
            config.update(**json.load(configFile))

        saveConfigFile(config)

        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file is missing!\n{sys.path[0]}../files/default_config.json")


def saveConfigFile(config: dict):

    with open(f"{sys.path[0]}/../files/config.json", "w") as configFile:
        json.dump(config, configFile, indent=4)
