import asyncio
import os
import Common.src.Constants as Const
import Common.src.Logging as Logging
import Common.src.RedisStreams as RedisStreams
import pymongo
import time
import threading

async def handle_user_request(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        #print(f"Received {message!r} from {addr!r}", flush=True)

        message = message.split(',')
        
        if (len(message) < 2):
            writer.write(''.encode())
            await writer.drain()
            continue

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
        Logging.log_add_funds(request[1], request[2])
        return await add_funds(request[1], request[2])

    elif request[0] == Const.BUY:
        Logging.log_buy(request[1], request[2], request[3])
        return await buy(request[1], request[2], request[3])

    elif request[0] == Const.COMMIT_BUY:
        Logging.log_commit_buy(request[1])
        return await commit_buy(request[1])

    elif request[0] == Const.CANCEL_BUY:
        Logging.log_cancel_buy(request[1])
        return await cancel_buy(request[1])

    elif request[0] == Const.SELL:
        Logging.log_sell(request[1], request[2], request[3])
        return await sell(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SELL:
        Logging.log_cancel_sell(request[1])
        return await cancel_sell(request[1])

    elif request[0] == Const.SET_BUY_AMOUNT:
        Logging.log_set_buy_amount(request[1], request[2], request[3])
        return await set_buy_amount(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SET_BUY:
        Logging.log_cancel_set_buy(request[1], request[2])
        return await cancel_set_buy(request[1], request[2])

    elif request[0] == Const.SET_BUY_TRIGGER:
        Logging.log_set_buy_trigger(request[1], request[2], request[3])
        return await set_buy_trigger(request[1], request[2], request[3])

    elif request[0] == Const.SET_SELL_AMOUNT:
        Logging.log_set_sell_amount(request[1], request[2], request[3])
        return await set_sell_amount(request[1], request[2], request[3])

    elif request[0] == Const.SET_SELL_TRIGGER:
        Logging.log_set_sell_trigger(request[1], request[2], request[3])
        return await set_sell_trigger(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SET_SELL:
        Logging.log_cancel_set_sell(request[1], request[2])
        return await cancel_set_sell(request[1], request[2])

    else:
        if Const.TRANSACTION_BYTE_TO_STR.__contains__(request[0]):
            request[0] = Const.TRANSACTION_BYTE_TO_STR[request[0]]
        else:
            request[0] = "Unknown"
        Logging.log_error(request, "Error: Unexpected request")
        return "Unexpected request: " + str(request[0])



async def add_funds(userid, amount):
    print("User ", userid, " add $", amount)

    res = db.User.update_one({"UserID": userid}, {"$inc": {"AccountBalance": float(amount)}})
    print(f"Update result: {res.raw_result!r}", flush=True)

    user = db['User'].find_one({"UserID": userid})
    print(f"DB user result: {user!r}", flush=True)

    if res.acknowledged:
        print("Add funds Ack")
        return "Add success"
    else:
        print("Add funds no ack")
        Logging.log_error(["ADD", userid], "Error: failed to add funds")
        return "Add fail"


async def quote(userid, stock_symbol):
    #global fetch_reader, fetch_writer
    print(db.list_collection_names())
    print(list(db.User.find()))
    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    stock = str(stock_symbol)

    if user is not None:
        print("User ", userid, " searched for ", stock, flush=True)
        timestamp = time.time()
        if(timestamp):
            user = db.User.update_one({"UserID": userid}, {"$set": {"Quote": {"Timestamp": timestamp,"Stock": stock_symbol}}})
            return "ok"
        else:
            Logging.log_error(["QUOTE", userid], "Error: Search could not be completed")
            print("User ", userid, " search could not be completed for ", stock, flush=True)
            return "SEARCHERROR"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["QUOTE", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def buy(userid, stock_symbol, amount):
    user = db.User.find_one({"UserID": userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
        if user["AccountBalance"] >= amount:
            print("User ", userid, " buy $", amount, " of ", stock_symbol, flush=True)
            timestamp = time.time()

            pending_buy = {"Timestamp": timestamp,
                           "Stock": stock_symbol,
                           "Amount": amount}

            result = db.User.update_one({"UserID": userid}, {"$set": {"PendingBuy": pending_buy}})

            print(f"DB user set result: {result.raw_result!r}", flush=True)

            return "ok"
        else:
            Logging.log_error(["BUY", userid], "Error: Insufficient funds")
            print("User ", userid, " non-sufficient funds (NSF)", flush=True)
            return "NSF"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["BUY", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"

async def commit_buy(userid):
    user = db.User.find_one({"UserID": userid})
    print(f"DB user result: {user!r}", flush=True)

    if user is not None:
        if not user.__contains__("PendingBuy") or user['PendingBuy'] is None:
            return "No pending buy"
        else:
            now = time.time()
            elapsed = now - int(user["PendingBuy"]["Timestamp"])

            print("Timestamps(then,now,elapsed): ", user["PendingBuy"]["Timestamp"], now, elapsed, flush=True)

            if elapsed <= 60:
                print("User ", userid, " Commit buy")
                db.User.update_one({"UserID": userid}, {"$inc": {"AccountBalance": -int(user["PendingBuy"]["Amount"])}})
                db.User.update_one({"UserID": userid}, {"$set": {"PendingBuy": None}})

                user = db.User.find_one({"UserID": userid})
                print(f"DB user after commit buy: {user!r}", flush=True)

                #todo: update stock portfolio
                return "Success"
            else:
                print("User ", userid, " Failed to commit buy. Elapsed: ", elapsed)
                Logging.log_error(["COMMIT_BUY", userid], "Error: Failed to commit buy; time elapsed: " + str(elapsed))
                return "Time window exceeded by " + str(elapsed - 60) + "s"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["COMMIT_BUY", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def cancel_buy(userid):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    if user is not None:
        if not user.__contains__("PendingBuy") or user['PendingBuy'] is None:
            return "No pending buy"
        else:
            now = time.time()
            elapsed = now - int(user["PendingBuy"]["Timestamp"])

            print("Timestamps(then,now,elapsed): ", user["PendingBuy"]["Timestamp"], now, elapsed, flush=True)

            if elapsed <= 60:
                user = db['User'].update_one({"UserID": userid}, {"$set": {"CancelBuy": {"Timestamp": now}}})
                return "ok"
            else:
                Logging.log_error(["CANCEL_BUY", userid], "Error: Cancel could not be completed")
                print("User ", userid, " cancel could not be completed", flush=True)
                return "CANCELERRORBUY"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["CANCEL_BUY", userid], "Error: Invalid user")
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
        if user["AccountBalance"] >= amount:
            print("User ", userid, " sells ", amount, " of ", stock_symbol, flush=True)
            timestamp = time.time()
            user = db['User'].update_one({"UserID": userid}, {"$set": {"PendingSell": {"Timestamp": timestamp,"Stock": stock_symbol,"Amount": amount}}})
            return "ok"
        else:
            Logging.log_error(["SELL", userid], "Error: Insufficient Stock Amount")
            print("User ", userid, " Insufficient stock amount (ISA)", flush=True)
            return "ISA"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["SELL", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def commit_sell(userid):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    if user is not None:
        if not user.__contains__("PendingSell") or user['PendingSell'] is None:
            return "No pending sell"
        else:
        # print("User ", userid, " committed buy command", flush=True)
            now = time.time()
            elapsed = now - int(user["PendingSell"]["Timestamp"])
            print("Timestamps(then,now,elapsed): ", user["PendingSell"]["Timestamp"], now, elapsed, flush=True)
        #check pending sell ~60s ago
            if elapsed <= 60:
                print("User ", userid, " Commit sell")
                db.User.update_one({"UserID": userid}, {"$inc": {"AccountBalance": int(user["PendingSell"]["Amount"])}})
                db.User.update_one({"UserID": userid}, {"$set": {"PendingSell": None}})

                user = db.User.find_one({"UserID": userid})
                print(f"DB user after commit sell: {user!r}", flush=True)

                #todo: update stock portfolio
                return "Success"
            else:
                Logging.log_error(["COMMIT_SELL", userid], "Error: Failed to commit sell; time elapsed: " + str(elapsed))
                print("User ", userid, " Failed to commit sell. Elapsed: ", elapsed)
                return "Time window exceeded by " + str(elapsed - 60) + "s"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["COMMIT_SELL", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def cancel_sell(userid):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    if user is not None:
        if not user.__contains__("PendingSell") or user['PendingSell'] is None:
            return "No pending sell"
        else:
            now = time.time()
            elapsed = now - int(user["PendingSell"]["Timestamp"])

            print("Timestamps(then,now,elapsed): ", user["PendingSell"]["Timestamp"], now, elapsed, flush=True)

            if elapsed <= 60:
                user = db['User'].update_one({"UserID": userid}, {"$set": {"CancelSell": {"Timestamp": now}}})
                return "ok"
            else:
                Logging.log_error(["CANCEL_SELL", userid], "Error: Cancel could not be completed")
                print("User ", userid, " cancel could not be completed", flush=True)
                return "CANCELERRORSELL"        
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["CANCEL_SELL", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def set_buy_amount(userid, stock_symbol, amount):
    amount = float(amount)
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    if user is not None:
        print("User ", userid, " is setting a buy for stock ", stock_symbol, " at price ", amount, flush=True)
        timestamp = time.time()
        print(timestamp)
        # check funds >= buy amount * stock price
        #user.funds >= amount_of_stocks * stock_price
        if user["AccountBalance"] >= amount:
            user = db['User'].update_one({"UserID": userid}, {"$set": {"SetBuyAmount": {"Timestamp": timestamp,"Stock": stock_symbol,"Amount": amount}}})
            return "ok"
        else:
            Logging.log_error(["SET_BUY_AMOUNT", userid], "Error: could not set a buy amount")
            print("User ", userid, " can not set automated buy for ", stock_symbol, flush=True)
            return "SETBUYERROR"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["SET_BUY_AMOUNT", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def cancel_set_buy(userid, stock_symbol):
    # check existing "set buy" for stock
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    if user is not None:
        print("User ", userid, " committed buy command", flush=True)
        timestamp = time.time()
        print(timestamp)
        #check pending sell ~60s ago
        if(timestamp):
            user = db['User'].update_one({"UserID": userid}, {"$set": {"CancelSetBuy": {"Timestamp": timestamp,"Stock": stock_symbol}}})
            return "ok"
        else:
            Logging.log_error(["CANCEL_SET_BUY", userid], "Error: Cancel could not be completed")
            print("User ", userid, " cancel could not be completed", flush=True)
            return "CANCELERRORSETBUY"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["CANCEL_SET_BUY", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def set_buy_trigger(userid, stock_symbol, amount):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
        print("User ", userid, " is setting a buy trigger for stock ", stock_symbol, " at price ", amount, flush=True)
        timestamp = time.time()
        print(timestamp)
        # check funds >= buy amount * stock price at trigger value
        if user["AccountBalance"] >= amount:
            user = db['User'].update_one({"UserID": userid}, {"$set": {"SetBuyTrigger": {"Timestamp": timestamp,"Stock": stock_symbol,"Amount": amount}}})
            return "ok"
        else:
            Logging.log_error(["SET_BUY_TRIGGER", userid], "Error: could not set a buy trigger")
            print("User ", userid, " can not set automated buy for ", stock_symbol, flush=True)
            return "SETBUYTRIGGERERROR"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["SET_BUY_TRIGGER", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def set_sell_amount(userid, stock_symbol, amount):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
        print("User ", userid, " is setting a sell for stock ", stock_symbol, " at price ", amount, flush=True)
        timestamp = time.time()
        print(timestamp)
        # check #of stocks owned >= stocks wanting to sell
        if user["AccountBalance"] >= amount:
            user = db['User'].update_one({"UserID": userid}, {"$set": {"SetSellAmount": {"Timestamp": timestamp,"Stock": stock_symbol,"Amount": amount}}})
            return "ok"
        else:
            Logging.log_error(["SET_SELL_AMOUNT", userid], "Error: could not set a sell amount")
            print("User ", userid, " can not set automated sell for ", stock_symbol, flush=True)
            return "SETSELLERROR"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["SET_BUY_AMOUNT", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def set_sell_trigger(userid, stock_symbol, amount):
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    amount = float(amount)

    if user is not None:
        print("User ", userid, " is setting a sell trigger for stock ", stock_symbol, " at price ", amount, flush=True)
        timestamp = time.time()
        print(timestamp)
        # check number of stocks owned >= number fo stocks wanting to sell
        if user["AccountBalance"] >= amount:
            user = db['User'].update_one({"UserID": userid}, {"$set": {"SetSellTrigger": {"Timestamp": timestamp,"Stock": stock_symbol,"Amount": amount}}})
            return "ok"
        else:
            Logging.log_error(["SET_SELL_TRIGGER", userid], "Error: could not set a sell trigger")
            print("User ", userid, " can not set automated sell for ", stock_symbol, flush=True)
            return "SETSELLTRIGGERERROR"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["SET_SELL_TRIGGER", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


async def cancel_set_sell(userid, stock_symbol):
    # check existing "set sell" for stock
    print(db.list_collection_names())
    print(list(db.User.find()))

    user = db['User'].find_one({"UserID":userid})

    print(f"DB user result: {user!r}", flush=True)

    if user is not None:
        print("User ", userid, " cancel set sell", flush=True)
        timestamp = time.time()
        print(timestamp)
        #check pending sell ~60s ago
        if(timestamp):
            user = db['User'].update_one({"UserID": userid}, {"$set": {"CancelSetSell": {"Timestamp": timestamp,"Stock": stock_symbol}}})
            return "ok"
        else:
            Logging.log_error(["CANCEL_SET_SELL", userid], "Error: Cancel could not be completed")
            print("User ", userid, " cancel could not be completed", flush=True)
            return "CANCELERRORSETSELL"
    else:
        print("User ", userid, " not found!", flush=True)
        Logging.log_error(["CANCEL_SET_SELL", userid], "Error: Invalid user")
        return "invalid user"

    return "unhandled error"


def main():

    try:
        RedisStreams.client.xgroup_create('command_in', 'tx', mkstream=True)
    except:
        print('exception in xgroup_create command_in')

    try:
        RedisStreams.client.xgroup_create('command_out', 'tx', mkstream=True)
    except:
        print('exception in xgroup_create command_out')

    while True:
        for _stream, messages in RedisStreams.client.xreadgroup('tx', RedisStreams.container_id, {'command_in': '>'}, 1, block=100):
            print('listen to stream: ', _stream)
            for message in messages:
                print(message, flush=True)

                response = handle_request(message[1])

                RedisStreams.client.xadd('command_out', {'response': response})
                RedisStreams.client.xack('command_in', 'tx', message[0])


#redis_listener = threading.Thread(target=RedisStreams.start_listener, args=('command_in', 'tx', handle_stream_in,))
#redis_listener.start()

#RedisStreams.write_to_stream('command_out', {'command': RedisStreams.container_id})

RedisStreams.client = RedisStreams.connect()
db_client = pymongo.MongoClient("router1", int(os.environ["MONGO_PORT"]))
db = db_client.DayTrading

main()

