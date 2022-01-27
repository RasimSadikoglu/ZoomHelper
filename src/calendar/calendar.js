const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, '../../config/data.json');

const time = document.getElementById('time');

time.innerText = new Date().toLocaleDateString(undefined, {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    weekday: 'long'
});

const meetings = JSON.parse(fs.readFileSync(dataPath));

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

const grid = document.getElementById('grid');

days.forEach((day, i) => {
    gridItem = document.createElement('div');
    gridItem.className = 'grid-item';
    gridItem.innerText = day;
    gridItem.style.gridRow = '1 / 1';
    gridItem.style.gridColumn = `${i + 1} / ${i + 1}`;
    
    grid.appendChild(gridItem);
});

const repetitiveMeetings = meetings.filter(m => m.weekDay !== null);

repetitiveMeetings.sort((m1, m2) => {
    if (m1.weekDay !== m2.weekDay) return m1.weekDay > m2.weekDay;
    return m1.time > m2.time;
});

let gridIndexes = [2, 2, 2, 2, 2, 2, 2];

repetitiveMeetings.forEach((meeting) => {
    gridItem = document.createElement('div');
    gridItem.className = 'grid-item';
    gridItem.innerText = meeting.name + '\n' + meeting.time;
    gridItem.id = 'meeting';
    
    let column = meeting.weekDay;
    let row = gridIndexes[column]++;

    console.log('%d - %d', column, row);

    gridItem.style.gridRow = `${row} / ${row}`;
    gridItem.style.gridColumn = `${column + 1} / ${column + 1}`;
    
    grid.appendChild(gridItem);
});