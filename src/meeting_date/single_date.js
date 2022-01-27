const MeetingDate = require('./meeting_date.js');

class SingleDate extends MeetingDate {
    constructor(date, time) {
        super();

        this.type = 'Single';
        
        this.date = date;
        this.time = time;
    }
    
    isTime(startOffset, endOffset) { return false; }

    isShow(timeWindow) { return false; }
}

module.exports = SingleDate;