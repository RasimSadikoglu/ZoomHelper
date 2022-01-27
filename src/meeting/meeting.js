class Meeting {
    constructor(name, id, password, date) {
        this.name = name;
        this.id = id;
        this.password = password;
        this.date = date;
    }
  
    openMeeting() {}
    
    isTime(startOffset, endOffset) { return this.date.isTime(); }

    isShow(timeWindow) { return this.date.isShow(timeWindow); }
}

module.exports = Meeting;