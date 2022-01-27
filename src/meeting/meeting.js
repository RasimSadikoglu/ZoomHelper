class Meeting {
    constructor(name, id, password, date) {
        this.name = name;
        this.id = id;
        this.password = password;
        this.date = date;
    }
    
    // Abstract
    openMeeting() {
    }
    
    checkTime() {
        this.date.checkTime();
    }
}

module.exports = Meeting;