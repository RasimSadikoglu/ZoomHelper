const SingleDate = require('./single_date');
const RepetitiveDate = require('./repetitive_date');

function createDate(date) {
    return new RepetitiveDate(
        date.weekDay,
        date.time
    );
}

module.exports = createDate;