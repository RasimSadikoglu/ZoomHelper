const Meeting = require('./meeting.js');

class Zoom extends Meeting {
    constructor(name, id, password, date) {
        this.platform = 'Zoom';
        
        super(name, id, password, date);
    }
    
    openMeeting() {}
}

module.exports = Zoom;