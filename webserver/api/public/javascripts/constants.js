const ADD = 0b0;
const QUOTE = 0b01;

const BUY = 0b010;
const COMMIT_BUY = 0b011;
const CANCEL_BUY = 0b100;

const SELL = 0b101;
const COMMIT_SELL = 0b110;
const CANCEL_SELL = 0b111;

const SET_BUY_AMOUNT = 0b1000;
const CANCEL_SET_BUY = 0b1001;
const SET_BUY_TRIGGER = 0b1010;

const SET_SELL_AMOUNT = 0b1011;
const SET_SELL_TRIGGER = 0b1100;
const CANCEL_SET_SELL = 0b1101;

const DUMPLOG = 0b1110;
const DISPLAY_SUMMARY = 0b1111;

//EXPORTS

module.exports.ADD = ADD;
module.exports.QUOTE = QUOTE;

module.exports.BUY = BUY;
module.exports.COMMIT_BUY = COMMIT_BUY;
module.exports.CANCEL_BUY = CANCEL_BUY;

module.exports.SELL = SELL;
module.exports.COMMIT_SELL = COMMIT_SELL;
module.exports.CANCEL_SELL = CANCEL_SELL;

module.exports.SET_BUY_AMOUNT = SET_BUY_AMOUNT;
module.exports.CANCEL_SET_BUY = CANCEL_SET_BUY;
module.exports.SET_BUY_TRIGGER = SET_BUY_TRIGGER;

module.exports.SET_SELL_AMOUNT = SET_SELL_AMOUNT;
module.exports.SET_SELL_TRIGGER = SET_SELL_TRIGGER;
module.exports.CANCEL_SET_SELL = CANCEL_SET_SELL;

module.exports.DUMPLOG = DUMPLOG;
module.exports.DISPLAY_SUMMARY = DISPLAY_SUMMARY;