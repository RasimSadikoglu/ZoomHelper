const Meeting = require('./meeting.js');

class Zoom extends Meeting {
    constructor(name, id, password, date) {
        super(name, id, password, date);
        
        this.platform = 'Zoom';
    }
    
    openMeeting() {}
}

module.exports = Zoom;