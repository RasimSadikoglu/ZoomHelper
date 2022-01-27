const Zoom = require('./zoom');
const createDate = require('../meeting_date/factory');

function createMeeting(meeting) {
    return new Zoom(
        meeting.name,
        meeting.id,
        meeting.password,
        createDate(meeting.date)
    );
}

module.exports = createMeeting;