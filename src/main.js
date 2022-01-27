module.exports = start;

const path = require('path');
const fs = require('fs');
const {ipcMain} = require('electron');

const createMeeting = require('./meeting/factory');

const dataPath = path.join(__dirname, '../config/data.json');
const calendarPath = path.join(__dirname, 'calendar/calendar.html');

const buildType = "dev";

// const numberOfDaysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
// const nameOfTheDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
// const nameOfTheMonths = [
//     'January', 'February', 'March', 'April',
//     'May', 'June', 'July', 'August',
//     'September', 'October', 'November', 'December'
// ];

let mainWindow = undefined;
let timeWindow = undefined;
let meetings = [];

function start(__mainWindow) {
    mainWindow = __mainWindow;

    mainWindow.loadURL(calendarPath);

    if (buildType === 'dev') mainWindow.webContents.toggleDevTools();

    buildMeetings(JSON.parse(fs.readFileSync(dataPath)));

    timeWindow = new Date();
    timeWindow.setDate(timeWindow.getDate() - timeWindow.getDay() + 1);
    timeWindow.setUTCHours(0, 0, 0, 0);

    drawCalendar();
}

function buildMeetings(jsonMeetings) {
    for (let i = 0; i < jsonMeetings.length; i++) {
        meetings.push(createMeeting(jsonMeetings[i]));
    }
}

function drawCalendar() {

    let grid = [];
    let currentDate = new Date(timeWindow.valueOf());

    for (let i = 0; i < 7; i++) {
        
        let filteredMeetings = meetings.filter(meeting => meeting.isShow(currentDate));

        filteredMeetings.sort((m1, m2) => m1.date.time > m2.date.time);

        let labels = [];

        labels.push({
            reference: undefined,
            name: getDateString(currentDate),
            type: 'date'
        });

        filteredMeetings.forEach(meeting => {
            labels.push({
                reference: meeting,
                name: `${meeting.name}\n${meeting.date.time}`,
                type: 'saved'
            });
        });

        grid.push(labels);

        currentDate.setDate(currentDate.getDate() + 1);
    }

    date = new Date().toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
    });

    sendMessage('calendar:draw', { date: date, grid: grid });
}

function getDateString(date) {
    let nameOfTheDay = date.toLocaleDateString(undefined, { weekday: 'long' });
    return `${nameOfTheDay}\n${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
}

function sendMessage(event, message) {

    mainWindow.webContents.on('did-finish-load', () => {
        mainWindow.webContents.send(event, message);
    });

}