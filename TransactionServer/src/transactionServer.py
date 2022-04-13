import asyncio
import Common.src.Cache as Cache
import Common.src.Constants as Const
import Common.src.Logging as Logging
import json
import os
import pymongo
import time


# TODO: check for malformed requests
async def handle_request(request):
    if request[b'command'] == b'ADD':
        Logging.log_add_funds(request[b'userID'], request[b'value'])
        return await add_funds(request[b'userID'].decode("utf-8"), request[b'value'].decode("utf-8"))

    elif request[b'command'] == b'BUY':
        Logging.log_buy(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))
        return await buy(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))

    elif request[b'command'] == b'COMMIT_BUY':
        Logging.log_commit_buy(request[b'userID'].decode("utf-8"))
        return await commit_buy(request[b'userID'].decode("utf-8"))

    elif request[b'command'] == b'CANCEL_BUY':
        Logging.log_cancel_buy(request[b'userID'].decode("utf-8"))
        return await cancel_buy(request[b'userID'].decode("utf-8"))

    elif request[b'command'] == b'SELL':
        Logging.log_sell(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))
        return await sell(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))

    elif request[b'command'] == b'COMMIT_SELL':
        Logging.log_commit_sell(request[b'userID'].decode("utf-8"))
        return await commit_sell(request[b'userID'].decode("utf-8"))

    elif request[b'command'] == b'CANCEL_SELL':
        Logging.log_cancel_sell(request[b'userID'].decode("utf-8"))
        return await cancel_sell(request[b'userID'].decode("utf-8"))

    elif request[b'command'] == b'SET_BUY_AMOUNT':
        Logging.log_set_buy_amount(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))
        return await set_buy_amount(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))

    elif request[b'command'] == b'CANCEL_SET_BUY':
        Logging.log_cancel_set_buy(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"))
        return await cancel_set_buy(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"))

    elif request[b'command'] == b'SET_BUY_TRIGGER':
        Logging.log_set_buy_trigger(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))
        return await set_buy_trigger(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))

    elif request[b'command'] == b'SET_SELL_AMOUNT':
        Logging.log_set_sell_amount(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))
        return await set_sell_amount(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))

    elif request[b'command'] == b'SET_SELL_TRIGGER':
        Logging.log_set_sell_trigger(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))
        return await set_sell_trigger(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"), request[b'value'].decode("utf-8"))

    elif request[b'command'] == b'CANCEL_SET_SELL':
        Logging.log_cancel_set_sell(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"))
        return await cancel_set_sell(request[b'userID'].decode("utf-8"), request[b'stock'].decode("utf-8"))

    else:
        Logging.log_error(request, "Error: Unexpected request")
        return "Unexpected request: " + request[b'command'].decode("utf-8")


def user_not_found(command, userid):
    err_msg = "Error: Invalid user"
    Logging.log_error([command, userid], err_msg)
    return err_msg


async def add_funds(userid, amount):
    user = db.User.find_one({"UserID": userid})
    if user is None:
        return user_not_found("ADD_FUNDS", userid)

    res = db.User.update_one({"UserID": userid}, {"$inc": {"AccountBalance": float(amount)}})
    Cache.client.hset(userid, Const.CACHE_BALANCE, user['AccountBalance'] + float(amount))

    if res.acknowledged:
        return "Add success"
    else:
        Logging.log_error(["ADD", userid], "Error: DB failed to add funds")
        return "Add failed"


async def quote(userid, stock):
    Cache.write_to_stream(Const.STREAM_QUOTE_IN, {'userID': userid, 'stock': stock})

    while not Cache.client.exists(stock):
        time.sleep(0.005)

    return float(Cache.client.get(stock))


async def buy(userid, stock, amount):
    if Cache.client.hexists(userid, Const.CACHE_BALANCE):
        balance = float(Cache.client.hget(userid, Const.CACHE_BALANCE))
    else:
        user = db.User.find_one({"UserID": userid})
        if user is None:
            return user_not_found("BUY", userid)
        else:
            balance = float(user['AccountBalance'])

    amount = float(amount)

    if balance < amount:
        err_msg = "Error: Insufficient funds"
        Logging.log_error(["BUY", userid], err_msg)
        return err_msg
    else:
        if Cache.client.exists(stock):
            stock_price = float(Cache.client.get(stock))
        else:
            stock_price = float(await quote(userid, stock))

        count = int(amount / stock_price)

        if count == 0:
            err_msg = "Error: Insufficient funds"
            Logging.log_error(["BUY", userid], err_msg)
            return err_msg

        timestamp = time.time()
        pending_buy = {"Timestamp": timestamp,
                       "Stock": stock,
                       "Count": count,
                       "Price": stock_price * count}

        Cache.client.hset(userid, Const.CACHE_PENDING_BUY, json.dumps(pending_buy))
        return "Purchase pending"


async def commit_buy(userid):
    if not Cache.client.hexists(userid, Const.CACHE_PENDING_BUY):
        err_msg = "Error: No pending stock purchase for user " + userid
        Logging.log_error(["COMMIT_BUY", userid], err_msg)
        return err_msg

    pending_buy = json.loads(Cache.client.hget(userid, Const.CACHE_PENDING_BUY))
    Cache.client.hdel(userid, Const.CACHE_PENDING_BUY)

    now = time.time()
    elapsed = now - int(pending_buy["Timestamp"])

    if elapsed > 60:
        Logging.log_error(["COMMIT_BUY", userid], "Error: Failed to commit buy; time elapsed: " + str(elapsed))
        return "Time window exceeded by " + str(elapsed - 60) + "s"

    user = db.User.find_one({"UserID": userid})
    if user is None:
        return user_not_found("COMMIT_BUY", userid)

    if Cache.client.hexists(userid, Const.CACHE_BALANCE):
        balance = float(Cache.client.hget(userid, Const.CACHE_BALANCE))
    else:
        balance = float(user['AccountBalance'])

    if balance < pending_buy['Price'] * pending_buy['Count']:
        err_msg = "Error: Insufficient funds; there must be a buy trigger set."
        Logging.log_error(["COMMIT_BUY", userid], err_msg)
        return err_msg

    db.User.update_one({"UserID": userid}, {"$inc": {"AccountBalance": -float(pending_buy["Price"])}})
    Cache.client.hset(userid, Const.CACHE_BALANCE, balance - float(pending_buy["Price"]))
    db.StockPortfolio.update_one({"UserID": userid}, {"$inc": {pending_buy['Stock']: float(pending_buy['Count'])}},
                                 upsert=True)
    return "Committed purchase"


async def cancel_buy(userid):
    if Cache.client.hexists(userid, Const.CACHE_PENDING_BUY):
        err_msg = "Error: No pending purchase for user " + userid
        Logging.log_error(["CANCEL_BUY", userid], err_msg)
        return err_msg

    Cache.client.hdel(userid, Const.CACHE_PENDING_BUY)
    return "Purchase cancelled"


async def sell(userid, stock, amount):
    user_portfolio = db.StockPortfolio.find_one({"UserID": userid})
    if user_portfolio is None:
        err_msg = "Error: No portfolio found for user " + userid
        Logging.log_error(["SELL", userid], err_msg)
        return err_msg

    if not user_portfolio.__contains__(stock):
        err_msg = "Error: No stock, " + stock + ", found for user " + userid
        Logging.log_error(["SELL", userid], err_msg)
        return err_msg

    if Cache.client.exists(stock):
        stock_price = float(Cache.client.get(stock))
    else:
        stock_price = float(await quote(userid, stock))

    amount = float(amount)
    count = int(amount / stock_price)

    if count > int(user_portfolio[stock]):
        err_msg = "Error: User, " + userid + ", does not own " + str(count) + " units of " + stock
        Logging.log_error(["SELL", userid], err_msg)
        return err_msg

    pending_sale = {"Timestamp": time.time(),
                    "Stock": stock,
                    "Count": count,
                    "Price": stock_price * count}

    Cache.client.hset(userid, Const.CACHE_PENDING_SELL, json.dumps(pending_sale))
    return "Sell pending"


async def commit_sell(userid):
    if not Cache.client.hexists(userid, Const.CACHE_PENDING_SELL):
        err_msg = "Error: No pending stock sale for user " + userid
        Logging.log_error(["COMMIT_SELL", userid], err_msg)
        return err_msg
    else:
        pending_sale = json.loads(Cache.client.hget(userid, Const.CACHE_PENDING_SELL))
        Cache.client.hdel(userid, Const.CACHE_PENDING_SELL)

    now = time.time()
    elapsed = now - int(pending_sale["Timestamp"])

    if elapsed > 60:
        Logging.log_error(["COMMIT_SELL", userid], "Error: Failed to commit sell; time elapsed: " + str(elapsed))
        return "Time window for sale exceeded by " + str(elapsed - 60) + "s"

    user = db.User.find_one({"UserID": userid})
    if user is None:
        return user_not_found("COMMIT_SELL", userid)

    user_portfolio = db.StockPortfolio.find_one({"UserID": userid})
    if user_portfolio[pending_sale['Stock']] < pending_sale['Count']:
        err_msg = "Error: Insufficient ownership of stock to complete sale. User must have an open sale for this stock."
        Logging.log_error(["COMMIT_SELL", userid], err_msg)
        return err_msg

    db.User.update_one({"UserID": userid}, {"$inc": {"AccountBalance": float(pending_sale["Price"])}})
    db.StockPortfolio.update_one({"UserID": userid}, {"$inc": {pending_sale['Stock']: -int(pending_sale['Count'])}})
    return "Committed Sale"
        

async def cancel_sell(userid):
    if not Cache.client.hexists(userid, Const.CACHE_PENDING_SELL):
        err_msg = "Error: No pending sale for user " + userid
        Logging.log_error(["CANCEL_SELL", userid], err_msg)
        return err_msg

    Cache.client.hdel(userid, Const.CACHE_PENDING_SELL)
    return "Sale cancelled"


async def set_buy_amount(userid, stock, amount):
    if Cache.client.hexists(userid, Const.CACHE_BALANCE):
        balance = Cache.client.hget(userid, Const.CACHE_BALANCE).decode('utf-8')
    else:
        user = db.User.find_one({"UserID": userid})
        if user is None:
            return user_not_found("SET_BUY_AMOUNT", userid)

        balance = user['AccountBalance']

    balance = float(balance)

    price_key = stock+"_buy_price"

    if Cache.client.hexists(price_key, userid):
        price = float(Cache.client.hget(price_key, userid).decode('utf-8'))
    else:
        user_open_buys = db.OpenBuyTransactions.find_one({"UserID": userid})
        if user_open_buys is None:
            err_msg = "Error: No trigger exists for user. Set a trigger before setting the number to purchase."
            Logging.log_error(["SET_BUY_AMOUNT", userid], err_msg)
            return err_msg
        elif user_open_buys[stock].__contains__('Price'):
            price = float(user_open_buys[stock]['Price'])
        else:
            err_msg = "Error: No trigger exists for user. Set a trigger before setting the number to purchase."
            Logging.log_error(["SET_BUY_AMOUNT", userid], err_msg)
            return err_msg

    amount = int(float(amount))

    if balance < amount * float(price):
        err_msg = "Error: NSF for amount and trigger set"
        Logging.log_error(["SET_BUY_AMOUNT", userid], err_msg)
        return err_msg

    stock_amount = stock + '.Amount'
    db.OpenBuyTransactions.update_one({"UserID": userid}, {"$set": {stock_amount: amount}}, upsert=True)

    Cache.client.hset(stock+"_buy_count", userid, amount)

    if Cache.client.hexists('buy_triggers', stock):
        Cache.client.hset('buy_triggers', stock, int(Cache.client.hget('buy_triggers', stock)) + 1)
    else:
        Cache.client.hset('buy_triggers', stock, 1)

    return "Buy amount set"


async def cancel_set_buy(userid, stock):
    key = stock+"_buy_count"
    if Cache.client.hexists(key, userid):
        Cache.client.hdel(key, userid)

    key = stock+"_buy_price"
    if Cache.client.hexists(key, userid):
        Cache.client.hdel(key, userid)

    if Cache.client.hexists('buy_triggers', stock):
        trigger_count = int(Cache.client.hget('triggers', stock))
        if trigger_count == 1:
            Cache.client.hdel('buy_triggers', stock)
        else:
            Cache.client.hset('buy_triggers', stock, trigger_count - 1)

    stock_amount = stock + '.Amount'
    db.OpenBuyTransactions.update_one({"UserID": userid}, {"$set": {stock_amount: 0}})
    return "Cancelled buy trigger"


async def set_buy_trigger(userid, stock, price):
    if Cache.client.hexists(userid, Const.CACHE_BALANCE):
        balance = Cache.client.hget(userid, Const.CACHE_BALANCE).decode('utf-8')
    else:
        user = db.User.find_one({"UserID": userid})
        if user is None:
            return user_not_found("SET_BUY_AMOUNT", userid)

        balance = user['AccountBalance']

    balance = float(balance)
    price = float(price)

    if balance < price:
        err_msg = "Error: could not set a buy trigger"
        Logging.log_error(["SET_BUY_TRIGGER", userid], err_msg)
        return err_msg
    else:
        stock_price = stock+".Price"
        db.OpenBuyTransactions.update_one({"UserID": userid}, {"$set": {stock_price: price}}, upsert=True)

        Cache.client.hset(stock + "_buy_price", userid, price)
        return "Buy trigger set"


async def set_sell_amount(userid, stock, amount):
    amount = int(float(amount))

    user_portfolio = db.StockPortfolio.find_one({"UserID": userid})
    if user_portfolio is None:
        err_msg = "Error: Cannot set sell amount, user owns no stock."
        Logging.log_error(["SET_SELL_AMOUNT", userid], err_msg)
        return err_msg
    else:
        if stock not in user_portfolio:
            err_msg = "Error: User does not own shares in " + stock
            Logging.log_error(["SET_SELL_AMOUNT", userid], err_msg)
            return err_msg
        elif int(user_portfolio[stock]) < amount:
            err_msg = "Error: User has fewer shares than the specified sell amount."
            Logging.log_error(["SET_SELL_AMOUNT", userid], err_msg)
            return err_msg

    stock_amount = stock+".Amount"
    db.OpenSellTransactions.update_one({"UserID": userid}, {"$set": {stock_amount: amount}}, upsert=True)

    Cache.client.hset(stock + "_sell_count", userid, amount)

    if Cache.client.hexists('sell_triggers', stock):
        Cache.client.hset('sell_triggers', stock, int(Cache.client.hget('sell_triggers', stock)) + 1)
    else:
        Cache.client.hset('sell_triggers', stock, 1)

    return "Sell amount set"


async def set_sell_trigger(userid, stock, price):
    user_portfolio = db.StockPortfolio.find_one({"UserID": userid})
    if user_portfolio is None:
        err_msg = "Error: Cannot set sell amount, user owns no stock."
        Logging.log_error(["SET_SELL_TRIGGER", userid], err_msg)
        return err_msg
    else:
        if stock not in user_portfolio:
            err_msg = "Error: User does not own shares in " + stock
            Logging.log_error(["SET_SELL_TRIGGER", userid], err_msg)
            return err_msg

    price = float(price)
    stock_price = stock+'.Price'
    db.OpenSellTransactions.update_one({"UserID": userid}, {"$set": {stock_price: price}}, upsert=True)

    Cache.client.hset(stock + "_sell_price", userid, price)
    return 'Sell trigger set'


async def cancel_set_sell(userid, stock):
    key = stock + "_buy_count"
    if Cache.client.hexists(key, userid):
        Cache.client.hdel(key, userid)

    key = stock + "_buy_price"
    if Cache.client.hexists(key, userid):
        Cache.client.hdel(key, userid)

    if Cache.client.hexists('sell_triggers', stock):
        trigger_count = int(Cache.client.hget('sell_triggers', stock))
        if trigger_count == 1:
            Cache.client.hdel('sell_triggers', stock)
        else:
            Cache.client.hset('sell_triggers', stock, trigger_count - 1)

    stock_amount = stock+".Amount"
    db.OpenBuyTransactions.update_one({"UserID": userid}, {"$set": {stock_amount: 0}})

    return 'Cancelled sell trigger'


async def main():

    try:
        Cache.client.xgroup_create('command_in', 'tx', mkstream=True)
    except:
        pass

    while True:
        for _stream, messages in Cache.client.xreadgroup('tx', Cache.container_id, {'command_in': '>'}, 1, block=30):
            for message in messages:
                response = await handle_request(message[1])
                Cache.client.xadd('command_out', {'response': response})
                Cache.client.xack('command_in', 'tx', message[0])


Cache.client = Cache.connect()
db = pymongo.MongoClient("router1", int(os.environ["MONGO_PORT"])).DayTrading
Logging.set_db(db)

asyncio.run(main())
