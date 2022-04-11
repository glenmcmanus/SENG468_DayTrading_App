import time

db = None

def set_db(database):
    global db
    db = database

def log_add_funds(userid, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "ADD",
               "username": userid,
               #"funds": "n/a" #do we need this?
            }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_buy(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "BUY",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_commit_buy(userid):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "COMMIT_BUY",
               "username": userid,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_cancel_buy(userid):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "CANCEL_BUY",
               "username": userid,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_sell(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SELL",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_commit_sell(userid):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "COMMIT_SELL",
               "username": userid,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_cancel_sell(userid):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "CANCEL_SELL",
               "username": userid,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_set_buy_amount(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SET_BUY_AMOUNT",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_cancel_set_buy(userid, StockSymbol):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "CANCEL_SET_BUY",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_set_buy_trigger(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SET_BUY_TRIGGER",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_set_sell_amount(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SET_SELL_AMOUNT",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_set_sell_trigger(userid, StockSymbol, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "SET_SELL_TRIGGER",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


def log_cancel_set_sell(userid, StockSymbol):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "CANCEL_SET_SELL",
               "username": userid,
               "stockSymbol": StockSymbol,
               #"funds": "n/a" #do we need this?
                 }


def log_error(request, userid):
    event = {  "LogType": "ErrorEventType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": request[0],
               "username": request[1],
            }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)
