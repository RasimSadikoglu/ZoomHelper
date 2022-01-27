const {ipcRenderer} = require('electron');

ipcRenderer.on('calendar:draw', (event, args) => {
    
    document.getElementById('time').innerHTML = args.date;

    const gridHTML = document.getElementById('grid');

    for (let column = 0; column < args.grid.length; column++) {
        let day = args.grid[column];

        for (let row = 0; row < day.length; row++) {
            let label = day[row];

            gridItem = document.createElement('div');
            gridItem.className = 'grid-item';
            gridItem.innerText = label.name;
            gridItem.style.gridRow = `${row + 1} / ${row + 1}`;
            gridItem.style.gridColumn = `${column + 1} / ${column + 1}`;
            gridItem.id = label.type;
            
            gridHTML.appendChild(gridItem);
        }
    }
});