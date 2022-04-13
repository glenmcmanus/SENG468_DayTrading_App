import time

db = None


def set_db(database):
    global db
    db = database


def log_add_funds(userid, amount):
    event = {
               "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "ADD",
               "username": userid,
               #"funds": "n/a" #do we need this?
            }

    db.EventLog.insert_one(event)


def log_buy(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "BUY",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_commit_buy(userid):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "COMMIT_BUY",
               "username": userid,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_cancel_buy(userid):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "CANCEL_BUY",
               "username": userid,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_sell(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SELL",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_commit_sell(userid):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "COMMIT_SELL",
               "username": userid,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_cancel_sell(userid):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "CANCEL_SELL",
               "username": userid,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_set_buy_amount(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SET_BUY_AMOUNT",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_cancel_set_buy(userid, StockSymbol):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "CANCEL_SET_BUY",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_set_buy_trigger(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SET_BUY_TRIGGER",
               "username": userid,
               "stockSymbol": StockSymbol
               #"funds": "n/a" #do we need this?
            }

    db.EventLog.insert_one(event)


def log_set_sell_amount(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SET_SELL_AMOUNT",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    db.EventLog.insert_one(event)


def log_set_sell_trigger(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SET_SELL_TRIGGER",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
            }

    db.EventLog.insert_one(event)


def log_cancel_set_sell(userid, StockSymbol):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "CANCEL_SET_SELL",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
            }

    db.EventLog.insert_one(event)


def log_quote(userid, stock, result):
    event = {"LogType": "QuoteServerType",
             "timestamp": str(time.time()),
             "server": "default",
             #todo
             #"transactionNum": request['transactionNum'],
             "price": result[0],
             "stockSymbol": stock,
             "username": userid,
             "quoteServerTime": result[-2],
             "cryptokey": result[-1]}

    db.EventLog.insert_one(event)


def log_error(request, err_msg):
    event = {"LogType": "ErrorEventType",
             "timestamp": str(time.time()),
             "server": "default",
             "command": request[0],
             "username": request[1],
             "errorMessage": err_msg}

    db.EventLog.insert_one(event)


#todo, add generic private method to handle insertion and common attributes
#def __log(event):
#    event['timestamp'] = str(time.time())
#    db.EventLog.insert_one(event)
