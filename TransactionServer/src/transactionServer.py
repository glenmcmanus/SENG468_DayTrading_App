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
    
    log_command(request)
#request[0] = command
#request[1] = userid
#request[2] = funds/stocksymbol
#request[3] = amount
    if request[0] == Const.ADD:
        return await add_funds(request[1], request[2])

    elif request[0] == Const.BUY:
        return await buy(request[1], request[2], request[3])

    elif request[0] == Const.COMMIT_BUY:
        return await commit_buy(request[1])

    elif request[0] == Const.CANCEL_BUY:
        return await cancel_buy(request[1])

    elif request[0] == Const.SELL:
        return await sell(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SELL:
        return await cancel_sell(request[1])

    elif request[0] == Const.SET_BUY_AMOUNT:
        return await set_buy_amount(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SET_BUY:
        return await cancel_set_buy(request[1], request[2])

    elif request[0] == Const.SET_BUY_TRIGGER:
        return await set_buy_trigger(request[1], request[2], request[3])

    elif request[0] == Const.SET_SELL_AMOUNT:
        return await set_sell_amount(request[1], request[2], request[3])

    elif request[0] == Const.SET_SELL_TRIGGER:
        return await set_sell_trigger(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SET_SELL:
        return await cancel_set_sell(request[1], request[2])

    else:
        log_error(request)
        return "Unexpected request: " + str(request[0])

def log_command(request):
    f = open("transactionLogFile.txt", "a")
    #log in the UserCommandType format
    f.write("eventCommand\n")
    f.write(str(time.time()) + "\n")
    f.write("server-0\n")
    f.write("0\n")
    f.write(request[0] + "\n")
    f.write(request[1] + "\n")
    if request[0] == Const.BUY or request[0] == Const.SELL or request[0] == Const.SET_BUY_AMOUNT or request[0] == Const.CANCEL_SET_BUY or request[0] == Const.SET_BUY_TRIGGER or request[0] == Const.SET_SELL_AMOUNT or request[0] == Const.SET_SELL_TRIGGER or Const.CANCEL_SET_SELL:
        f.write(request[2] + "\n")
    else:
        f.write("NONE\n")
    f.write("filename\n")
    if request[0] == Const.ADD:
        f.write(str(request[2] + "\n\n"))
    else:
        f.write("NONE\n\n")
    f.close()

def log_error(request):
    f = open("transactionLogFile.txt", "a")
    #log in the ErrorEventType format
    f.write("eventError\n")
    f.write(str(time.time()) + "\n")
    f.write("server-0\n")
    f.write("0\n")
    f.write(request[0] + "\n")
    f.write(request[1] + "\n")
    if request[0] == Const.BUY or request[0] == Const.SELL or request[0] == Const.SET_BUY_AMOUNT or request[0] == Const.CANCEL_SET_BUY or request[0] == Const.SET_BUY_TRIGGER or request[0] == Const.SET_SELL_AMOUNT or request[0] == Const.SET_SELL_TRIGGER or Const.CANCEL_SET_SELL:
        f.write(request[2] + "\n")
    else:
        f.write("NONE\n")
    f.write("filename\n")
    if request[0] == Const.ADD:
        f.write(str(request[2] + "\n"))
    else:
        f.write("NONE\n")
    f.write("ERROR: Unexpected command\n\n")


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
        return "Add fail"


async def quote(userid, stock_symbol):
    global fetch_reader, fetch_writer


def log_add_funds():
    pass


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
            print("User ", userid, " non-sufficient funds (NSF)", flush=True)
            return "NSF"
    else:
        print("User ", userid, " not found!", flush=True)
        return "invalid user"

    return "unhandled error"

async def commit_buy(userid):
    # check pending buy <= 60 seconds ago
    print("User ", userid, " committed buy command")
    return "todo: implement commit buy"


async def cancel_buy(userid):
    # check pending buy <= 60 seconds ago
    print("User ", userid, " cancelled their buy command")
    return "todo: implement cancel buy"


async def sell(userid, stock_symbol, amount):
    # check stock amount >= sell amount
    print("User ", userid, " sell $", amount, " of ", stock_symbol)
    return "todo: implement sell"


async def commit_sell(userid):
    # check pending sell <= 60 seconds ago
    print("User ", userid, " committed sell command")
    return "todo: implement commit sell"


async def cancel_sell(userid):
    # check pending sell <= 60 seconds ago
    print("User ", userid, " cancelled sell command")
    return "todo: implement cancel sell"


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
