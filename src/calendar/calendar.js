const {ipcRenderer} = require('electron');

initialize();

function initialize() {
    document.getElementById('back').addEventListener('click', () => {
        ipcRenderer.send('calendar:timeWindow', -7);
    });

    document.getElementById('next').addEventListener('click', () => {
        ipcRenderer.send('calendar:timeWindow', 7);
    });

    document.getElementById('time').addEventListener('click', () => {
        ipcRenderer.send('calendar:timeWindow', 0);
    });
}

ipcRenderer.on('calendar:draw', (event, args) => {

    console.log(args.date);
    
    document.getElementById('time').innerHTML = args.date;

    const gridHTML = document.getElementById('grid');

    gridHTML.innerHTML = '';

    for (let column = 0; column < args.grid.length; column++) {
        let day = args.grid[column];

        for (let row = 0; row < day.length; row++) {
            let label = day[row];

            gridItem = document.createElement('div');
            gridItem.className = 'grid-item';
            gridItem.innerText = label.name;
            gridItem.style.gridRow = `${row + 1} / ${row + 1}`;
            gridItem.style.gridColumn = `${column + 1} / ${column + 1}`;
            gridItem.id = label.state;

            if (label.state !== 'date' && label.state !== 'today') {
                gridItem.addEventListener('click', (event) => {
                    ipcRenderer.send('calendar:click', { button: 'left', meeting: label.referance });
                });
            }

            if (label.state !== 'date' && label.state !== 'today') {
                gridItem.addEventListener('contextmenu', (event) => {
                    ipcRenderer.send('calendar:click', { button: 'right', meeting: label.referance });
                });
            }
            
            gridHTML.appendChild(gridItem);
        }
    }
});