const MeetingDate = require('./meeting_date.js');

class SingleDate extends MeetingDate {
    constructor(year, month, day, time) {
        super();

        this.type = 'Single';
        
        this.year = year;
        this.month = month;
        this.day = day;
        this.time = time;
    }
    
    checkTime() {}
}

module.exports = SingleDate;