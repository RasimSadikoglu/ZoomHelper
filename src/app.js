const main = require('./main.js');
const {app, BrowserWindow} = require('electron');

app.on('ready', () => {

    const mainWindow = new BrowserWindow({
        width: 1000,
        height: 600,
        title: 'Meeting Helper',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    }); 

    main(mainWindow);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit()
    }
});