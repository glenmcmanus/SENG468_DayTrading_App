ADD = 0b0
QUOTE = 0b01
BUY = 0b010
COMMIT_BUY = 0b011
CANCEL_BUY = 0b100
SELL = 0b101
COMMIT_SELL = 0b110
CANCEL_SELL = 0b111
SET_BUY_AMOUNT = 0b1000
CANCEL_SET_BUY = 0b1001
SET_BUY_TRIGGER = 0b1010
SET_SELL_AMOUNT = 0b1011
SET_SELL_TRIGGER = 0b1100
CANCEL_SET_SELL = 0b1101
DUMPLOG = 0b1110
DISPLAY_SUMMARY = 0b1111

ADD_STR = "ADD"
QUOTE_STR = "QUOTE"
BUY_STR = "BUY"
COMMIT_BUY_STR = "COMMIT_BUY"
CANCEL_BUY_STR = "CANCEL_BUY"
SELL_STR = "SELL"
COMMIT_SELL_STR = "COMMIT_SELL"
CANCEL_SELL_STR = "CANCEL_SELL"
SET_BUY_AMOUNT_STR = "SET_BUY_AMOUNT"
CANCEL_SET_BUY_STR = "CANCEL_SET_BUY"
SET_BUY_TRIGGER_STR = "SET_BUY"
SET_SELL_AMOUNT_STR = "SET_SELL_AMOUNT"
SET_SELL_TRIGGER_STR = "SET_SELL_TRIGGER"
CANCEL_SET_SELL_STR = "CANCEL_SET_SELL"
DUMPLOG_STR = "DUMPLOG"
DISPLAY_SUMMARY_STR = "DISPLAY_SUMMARY"

TRANSACTION_STR_TO_BYTE = {
    ADD_STR: ADD,
    QUOTE_STR: QUOTE,
    BUY_STR: BUY,
    COMMIT_BUY_STR: COMMIT_BUY,
    CANCEL_BUY_STR: CANCEL_BUY,
    SELL_STR: SELL,
    COMMIT_SELL_STR: COMMIT_SELL,
    CANCEL_SELL_STR: CANCEL_SELL,
    SET_BUY_AMOUNT_STR: SET_BUY_AMOUNT,
    CANCEL_SET_BUY_STR: CANCEL_SET_BUY,
    SET_BUY_TRIGGER_STR: SET_BUY_TRIGGER,
    SET_SELL_AMOUNT_STR: SET_SELL_AMOUNT,
    SET_SELL_TRIGGER_STR: SET_SELL_TRIGGER,
    CANCEL_SET_SELL_STR: CANCEL_SET_SELL,
    DUMPLOG_STR: DUMPLOG,
    DISPLAY_SUMMARY_STR: DISPLAY_SUMMARY
}