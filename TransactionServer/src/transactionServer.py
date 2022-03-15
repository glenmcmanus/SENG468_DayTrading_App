import asyncio
import datetime
import os
import Common.src.Constants as Const
import pymongo
import time

db_client = pymongo.MongoClient(os.environ["M_ROUTER1_IP"], 27017)
db = db_client.DayTrading

async def handle_user_request(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}", flush=True)

        message = message.split(',')

        message[0] = int(message[0])

        response = await handle_request(message)

        response = message[1] + ',' + response

        print(f"Send: {response!r}")
        writer.write(response.encode())
        await writer.drain()


# TODO: check for malformed requests
async def handle_request(request):
#request[0] = command
#request[1] = userid
#request[2] = funds/stocksymbol
#request[3] = amount
    if request[0] == Const.ADD:
        log_add_funds(request[1], request[2])
        return await add_funds(request[1], request[2])

    elif request[0] == Const.BUY:
        log_buy(request[1], request[2], request[3])
        return await buy(request[1], request[2], request[3])

    elif request[0] == Const.COMMIT_BUY:
        log_commit_buy(request[1])
        return await commit_buy(request[1])

    elif request[0] == Const.CANCEL_BUY:
        log_cancel_buy(request[1])
        return await cancel_buy(request[1])

    elif request[0] == Const.SELL:
        log_sell(request[1], request[2], request[3])
        return await sell(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SELL:
        log_cancel_sell(request[1])
        return await cancel_sell(request[1])

    elif request[0] == Const.SET_BUY_AMOUNT:
        log_set_buy_amount(request[1], request[2], request[3])
        return await set_buy_amount(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SET_BUY:
        log_cancel_set_buy(request[1], request[2])
        return await cancel_set_buy(request[1], request[2])

    elif request[0] == Const.SET_BUY_TRIGGER:
        log_set_buy_trigger(request[1], request[2], request[3])
        return await set_buy_trigger(request[1], request[2], request[3])

    elif request[0] == Const.SET_SELL_AMOUNT:
        log_set_sell_amount(request[1], request[2], request[3])
        return await set_sell_amount(request[1], request[2], request[3])

    elif request[0] == Const.SET_SELL_TRIGGER:
        log_set_sell_trigger(request[1], request[2], request[3])
        return await set_sell_trigger(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SET_SELL:
        log_cancel_set_sell(request[1], request[2])
        return await cancel_set_sell(request[1], request[2])

    else:
        log_error(request, "Error: Unexpected request")
        return "Unexpected request: " + str(request[0])

def log_add_funds(userid, amount):
    event = {  "LogType": "UserCommandType",
               "timestamp": str(time.time()),
               "server": "default",
               "command": "ADD",
               "username": userid,
               "stockSymbol": StockSymbol,
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
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
               "funds": "n/a" #do we need this?
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)

def log_error(request, errorMessage):
    event = {  "LogType": "ErrorEventType",
               "timestamp": str(time.time()),
               "server": "default", 
               "command": request[0],
               "username": request[1],
               "errorMessage": errorMessage
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)

def log_transaction(userid, funds):
    event = {  "LogType": "AccountTransactionType",
               "timestamp": str(time.time()),
               "server": "default", 
               "username": userid,
               "funds": funds
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)

def log_quote():
    event = {  "LogType": "QuoteServerType",
               "timestamp": str(time.time()),
               "server": "default", 
               "price": price,
               "stockSymbol": stockSymbol,
               "username": userid,
               "quoteServerTime": quoteServerTime,
               "cryptokey": cryptokey
                 }

    eventLog = db['EventLog']
    event_id = eventLog.insert_one(event).inserted_id
    newlog = db['EventLog'].find_one({"username":userid})
    print(f"DB log result: {newlog!r}", flush=True)


async def add_funds(userid, amount):
    print("User ", userid, " add $", amount)

    res = db.Users.update_one({"UserID":userid}, {"$inc" : {"AccountBalance":float(amount)}})
    print(res, flush=True)

    result = userid
    if res.acknowledged:
        print("Add funds Ack")
        return "Add success"
    else:
        print("Add funds no ack")
        log_error({"ADD", userid}, "Error: failed to add funds")
        return "Add fail"


async def quote(userid, stock_symbol):
     global fetch_reader, fetch_writer
     
    print(db.list_collection_names())
    print(list(db.User.find()))
    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    stock = str(stock_symbol)

    if user is not None:
        print("User ", userid, " searched for ", stock, flush=True)
            timestamp = datetime.datetime.utcnow()
            user = db['User'].update_one({"UserID": userid}, {"$set": {"Quote": {"Timestamp": timestamp,"Stock": stock_symbol}}})
            return "ok"
        else:
            log_error({"QUOTE", userid}, "Error: Search could not be completed")
            print("User ", userid, " search could not be completed for ", stock, flush=True)
            return "SEARCHERROR"
    else:
        print("User ", userid, " not found!", flush=True)
        log_error({"QUOTE", userid}, "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def buy(userid, stock_symbol, amount):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
        if user["AccountBalance"] >= amount:
            print("User ", userid, " buy $", amount, " of ", stock_symbol, flush=True)
            timestamp = datetime.datetime.utcnow()
            user = db['User'].update_one({"UserID": userid}, {"$set": {"PendingBuy": {"Timestamp": timestamp,
                                                                                    "Stock": stock_symbol,
                                                                                    "Amount": amount}}})
            return "ok"
        else:
            log_error({"BUY", userid}, "Error: Insufficient funds")
            print("User ", userid, " non-sufficient funds (NSF)", flush=True)
            return "NSF"
    else:
        print("User ", userid, " not found!", flush=True)
        log_error({"BUY", userid}, "Error: Invalid user")
        return "invalid user"

    return "unhandled error"

async def commit_buy(userid):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
         print("User ", userid, " committed buy command", flush=True)
        timestamp = datetime.datetime.utcnow()
        print(timestamp)
        #check pending buy ~60s ago
        if(timestamp)
            user = db['User'].update_one({"UserID": userid}, {"$set": {"CommitBuy": {"Timestamp": timestamp}}})
            return "ok"
        else:
            log_error({"COMMIT_BUY", userid}, "Error: Commit could not be completed")
            print("User ", userid, " commit could not be completed", flush=True)
            return "COMMITERRORBUY"
    else:
        print("User ", userid, " not found!", flush=True)
        log_error({"COMMIT_BUY", userid}, "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def cancel_buy(userid):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
         print("User ", userid, " committed buy command", flush=True)
        timestamp = datetime.datetime.utcnow()
        print(timestamp)
        #check pending buy ~60s ago
        if(timestamp)
            user = db['User'].update_one({"UserID": userid}, {"$set": {"CancelBuy": {"Timestamp": timestamp}}})
            return "ok"
        else:
            log_error({"CANCEL_BUY", userid}, "Error: Cancel could not be completed")
            print("User ", userid, " cancel could not be completed", flush=True)
            return "CANCELERRORBUY"
    else:
        print("User ", userid, " not found!", flush=True)
        log_error({"CANCEL_BUY", userid}, "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def sell(userid, stock_symbol, amount):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
        #Not exactly sure how to get User's amount of a certain stock
        if user["Amount"] >= amount:
            print("User ", userid, " sells ", amount, " of ", stock_symbol, flush=True)
            timestamp = datetime.datetime.utcnow()
            user = db['User'].update_one({"UserID": userid}, {"$set": {"PendingSell": {"Timestamp": timestamp,"Stock": stock_symbol,"Amount": amount}}})
            return "ok"
        else:
            log_error({"SELL", userid}, "Error: Insufficient Stock Amount")
            print("User ", userid, " Insufficient stock amount (ISA)", flush=True)
            return "ISA"
    else:
        print("User ", userid, " not found!", flush=True)
        log_error({"SELL", userid}, "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def commit_sell(userid):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
         print("User ", userid, " committed buy command", flush=True)
        timestamp = datetime.datetime.utcnow()
        print(timestamp)
        #check pending sell ~60s ago
        if(timestamp)
            user = db['User'].update_one({"UserID": userid}, {"$set": {"CommitSell": {"Timestamp": timestamp}}})
            return "ok"
        else:
            log_error({"COMMIT_SELL", userid}, "Error: Commit could not be completed")
            print("User ", userid, " commit could not be completed", flush=True)
            return "COMMITERRORSELL"
    else:
        print("User ", userid, " not found!", flush=True)
        log_error({"COMMIT_SELL", userid}, "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def cancel_sell(userid):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
         print("User ", userid, " committed buy command", flush=True)
        timestamp = datetime.datetime.utcnow()
        print(timestamp)
        #check pending sell ~60s ago
        if(timestamp)
            user = db['User'].update_one({"UserID": userid}, {"$set": {"CancelSell": {"Timestamp": timestamp}}})
            return "ok"
        else:
            log_error({"CANCEL_SELL", userid}, "Error: Cancel could not be completed")
            print("User ", userid, " cancel could not be completed", flush=True)
            return "CANCELERRORSELL"
    else:
        print("User ", userid, " not found!", flush=True)
        log_error({"CANCEL_SELL", userid}, "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def set_buy_amount(userid, stock_symbol, amount):
    # check funds >= buy amount * stock price
    print("User ", userid, " auto buy ", stock_symbol, " up to quantity ", amount)
    return "todo: implement set buy amount"


async def cancel_set_buy(userid, stock_symbol):
    # check existing "set buy" for stock
    print("User ", userid, " cancel auto purchase of ", stock_symbol)
    return "todo: implement cancel set buy"


async def set_buy_trigger(userid, stock_symbol, amount):
    # check buy amount set
    print("User ", userid, " set trigger to purchase ", stock_symbol, " when price <= $", amount)
    return "todo: implement set buy trigger"


async def set_sell_amount(userid, stock_symbol, amount):
    # check stock quantity >= amount
    print("User ", userid, " auto sell ", stock_symbol, " up to quantity ", amount)
    return "todo: implement set sell amount"


async def set_sell_trigger(userid, stock_symbol, amount):
    # check sell amount set
    print("User ", userid, " set trigger to sell ", stock_symbol, " when price >= ", amount)
    return "todo: implement set sell trigger"


async def cancel_set_sell(userid, stock_symbol):
    # check existing "set sell" for stock
    print("User ", userid, " cancel auto sale of ", stock_symbol)
    return "todo: implement cancel set sell"


async def main():

    if os.environ.__contains__("TRANSACTION_IP"):
        print(os.environ["TRANSACTION_IP"])
        my_ip = os.environ["TRANSACTION_IP"]
    else:
        my_ip = "127.0.0.1"

    if os.environ.__contains__("TRANSACTION_PORT"):
        print(os.environ["TRANSACTION_PORT"])
        my_port = os.environ["TRANSACTION_PORT"]
    else:
        my_port = 8889

   # global fetch_reader, fetch_writer
   # fetch_reader, fetch_writer = asyncio.open_connection(
   #         os.environ["FETCH_IP"], os.environ["FETCH_PORT"])

    server = await asyncio.start_server(
        handle_user_request, my_ip, my_port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}', flush=True)

    async with server:
        await server.serve_forever()


asyncio.run(main())
