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
let actionHistory = [];

let isLoaded = false;

function start(__mainWindow) {
    mainWindow = __mainWindow;

    mainWindow.loadURL(calendarPath);

    // if (buildType === 'dev') mainWindow.webContents.toggleDevTools();

    buildMeetings(JSON.parse(fs.readFileSync(dataPath)));

    timeWindow = new Date();
    timeWindow.setUTCDate(timeWindow.getUTCDate() - timeWindow.getUTCDay() + 1);
    timeWindow.setUTCHours(0, 0, 0, 0);

    drawCalendar();
}

function buildMeetings(jsonMeetings) {
    for (let i = 0; i < jsonMeetings.length; i++) {

        const meeting = createMeeting(jsonMeetings[i]);

        meetings.push({
            referance: meeting,
            name: `${meeting.name}\n${meeting.date.time}`,
            initial: JSON.stringify(meeting),
            state: 'saved'
        });
    }
}

function drawCalendar() {

    let grid = [];
    let currentDate = new Date(timeWindow.valueOf());

    dateOfToday = new Date();
    dateOfToday.setUTCHours(0, 0, 0, 0);

    for (let i = 0; i < 7; i++) {
        
        let filteredMeetings = meetings.filter(meeting => meeting.referance.isShow(currentDate));

        filteredMeetings.sort((m1, m2) => m1.referance.date.time > m2.referance.date.time);

        let labels = [];

        labels.push({
            reference: undefined,
            name: getDateString(currentDate),
            state: currentDate.toDateString() === dateOfToday.toDateString() ? 'today' : 'date'
        });

        labels.push(...filteredMeetings);

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
    
    if (!isLoaded) {
        mainWindow.webContents.on('did-finish-load', () => {
            mainWindow.webContents.send(event, message);
            isLoaded = true;
        });
    } else {
        mainWindow.webContents.send(event, message);
    }
}

ipcMain.on('calendar:timeWindow', (event, args) => {
    if (args === 0) {

    } else {
        timeWindow.setUTCDate(timeWindow.getUTCDate() + args);
    }

    drawCalendar();
});

ipcMain.on('calendar:click', (event, args) => {
    if (args.button === 'right') {
        
        const meeting = meetings.find(meeting => JSON.stringify(meeting.referance) === JSON.stringify(args.meeting));
        
        if (meeting.state !== 'delete') {
            meeting.state = 'delete';
        } else {
            meeting.state = JSON.stringify(meeting.referance) === meeting.initial ? 'saved' : 'updated';
        }
    }

    drawCalendar();
});