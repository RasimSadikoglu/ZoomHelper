module.exports = start;

const path = require('path');
const fs = require('fs');

const dataPath = path.join(__dirname, '../config/data.json');
const buildType = "dev";

function start(mainWindow) {
    mainWindow.loadURL(path.join(__dirname, 'calendar/calendar.html'));

    if (buildType === 'dev') mainWindow.webContents.toggleDevTools();

    let meetings = buildMeetings(JSON.parse(fs.readFileSync(dataPath)));
}

function buildMeetings(jsonMeetings) {}