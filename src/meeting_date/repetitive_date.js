const MeetingDate = require('./meeting_date.js');

class RepetitiveDate extends MeetingDate {
    constructor(weekDay, time) {
        super();
        
        this.type = 'Repetitive';
        
        this.weekDay = weekDay;
        this.time = time;
    }
    
    checkTime() {}
}

module.exports = RepetitiveDate;