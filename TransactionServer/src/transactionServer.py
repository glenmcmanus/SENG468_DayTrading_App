import asyncio
import os
import Common.src.Constants as Const
import pymongo
import pprint

db_client = pymongo.MongoClient(os.environ["M_ROUTER1_IP"], 27017)
db = db_client.DayTrading

fetch_reader, fetch_writer = await asyncio.open_connection(
            os.environ["FETCH_IP"], os.environ["FETCH_PORT"])

async def handle_user_request(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    message = message.split(',')

    message[0] = int(message[0])

    response = await handle_request(message)

    print(f"Send: {response!r}")
    writer.write(response.encode())
    await writer.drain()

    print("Close the connection")
    writer.close()


# TODO: check for malformed requests
async def handle_request(request):
    if request[0] == Const.ADD:
        return await add_funds(request[1], request[2])

    elif request[0] == Const.QUOTE:
        return await quote(request[1], request[2])

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
        return await cancel_set_buy(request[1], request[2], request[3])

    elif request[0] == Const.SET_BUY_TRIGGER:
        return await set_buy_trigger(request[1], request[2], request[3])

    elif request[0] == Const.SET_SELL_AMOUNT:
        return await set_sell_amount(request[1], request[2], request[3])

    elif request[0] == Const.SET_SELL_TRIGGER:
        return await set_sell_trigger(request[1], request[2], request[3])

    elif request[0] == Const.CANCEL_SET_SELL:
        return await cancel_set_sell(request[1], request[2])

    else:
        return "Unexpected request: " + str(request[0])


async def add_funds(userid, amount):
    print("User ", userid, " add $", amount)

    res = db.Users.update_one({"UserID":userid}, {"$inc" : {"AccountBalance":float(amount)}})
    pprint(res)

    if res.acknowledged:
        print("Add funds Ack")
    else:
        print("Add funds no ack")

    return "Added funds"


async def quote(userid, stock_symbol):
    print("User ", userid, " get quote for ", stock_symbol)

    message = ",".join(stock_symbol, userid)

    print(f'Send: {message!r}')
    fetch_writer.write(message.encode())
    await fetch_writer.drain()

    data = await fetch_reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    fetch_writer.close()
    await fetch_writer.wait_closed()

    data = data.decode()

    return data


async def buy(userid, stock_symbol, amount):

    user = db.Users.find_one({"UserID":userid})

    #this is wrong, we need to commit buy.. oops!
    if user["AccountBalance"] >= amount:


        print("User ", userid, " buy $", amount, " of ", stock_symbol)
        user = db.Users.update_one({"UserID":userid}, {"$inc" : {"AccountBalance":float(amount)}})
        return userid + " confirm purchase of $" + amount + " of " + stock_symbol
    else:
        print("User ", userid, "insufficient funds, balance: ", user["AccountBalance"])
        return userid + " insufficient funds; deny purchase of $" + amount + " of " + stock_symbol


async def commit_buy(userid):
    # check pending buy <= 60 seconds ago
    print("User ", userid, " committed buy command")
    return userid + " committed buy command"


async def cancel_buy(userid):
    # check pending buy <= 60 seconds ago
    print("User ", userid, " cancelled their buy command")
    return userid + " cancelled their buy command"


async def sell(userid, stock_symbol, amount):
    # check stock amount >= sell amount
    print("User ", userid, " sell $", amount, " of ", stock_symbol)
    return userid + " confirm sale of $" + amount + " of " + stock_symbol


async def commit_sell(userid):
    # check pending sell <= 60 seconds ago
    print("User ", userid, " committed sell command")
    return userid + " committed sell command"


async def cancel_sell(userid):
    # check pending sell <= 60 seconds ago
    print("User ", userid, " cancelled sell command")
    return userid + " cancelled sell command"


async def set_buy_amount(userid, stock_symbol, amount):
    # check funds >= buy amount * stock price
    print("User ", userid, " auto buy ", stock_symbol, " up to quantity ", amount)
    return userid + " set buy amount $" + amount + " for " + stock_symbol


async def cancel_set_buy(userid, stock_symbol):
    # check existing "set buy" for stock
    print("User ", userid, " cancel auto purchase of ", stock_symbol)
    return userid + " cancel auto purchase of " + stock_symbol


async def set_buy_trigger(userid, stock_symbol, amount):
    # check buy amount set
    print("User ", userid, " set trigger to purchase ", stock_symbol, " when price <= $", amount)
    return userid + " trigger set for " + stock_symbol + " <= $" + amount


async def set_sell_amount(userid, stock_symbol, amount):
    # check stock quantity >= amount
    print("User ", userid, " auto sell ", stock_symbol, " up to quantity ", amount)
    return userid + " sell up to $" + amount + " of " + stock_symbol


async def set_sell_trigger(userid, stock_symbol, amount):
    # check sell amount set
    print("User ", userid, " set trigger to sell ", stock_symbol, " when price >= ", amount)
    return userid + " set sell trigger for " + stock_symbol + " at $" + amount


async def cancel_set_sell(userid, stock_symbol):
    # check existing "set sell" for stock
    print("User ", userid, " cancel auto sale of ", stock_symbol)
    return userid + " cancel auto sale of " + stock_symbol;


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


    server = await asyncio.start_server(
        handle_user_request, my_ip, my_port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}', flush=True)

    async with server:
        await server.serve_forever()


asyncio.run(main())
