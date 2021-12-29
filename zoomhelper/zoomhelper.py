import data

def run():

    config = data.readConfigFile()
    startTimeOffset, endTimeOffset = config['startTimeOffset'], config['endTimeOffset']

    meetings = [m for m in data.readDataFile()[1] if m.check(startTimeOffset, endTimeOffset)]

    meetings[0].open()

if __name__ == '__main__':
    run()