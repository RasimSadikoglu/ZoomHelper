const MeetingDate = require('./meeting_date.js');

class RepetitiveDate extends MeetingDate {
    constructor(weekDay, time) {
        super();
        
        this.type = 'Repetitive';
        
        this.weekDay = weekDay;
        this.time = time;
    }
    
    isTime(startOffset, endOffset) { return false; }

    isShow(timeWindow) {
        let currentDay = timeWindow.getDay();

        return this.weekDay === currentDay;
    }
}

module.exports = RepetitiveDate;