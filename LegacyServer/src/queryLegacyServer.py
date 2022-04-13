import asyncio
import Common.src.Cache as Cache
import Common.src.Constants as Const
import Common.src.Logging as Logging
import os
from subprocess import Popen, PIPE, run
import threading
import time

#This code is incomplete

#TODO:
#receive input from transaction server
#reformat ouput in some way
#send output to transaction server (possibly a different file)


def log_request(response):
    #eventually must write to DB
    f = open("queryLogFile.txt", "a")
    f.write("eventQuery\n")
    f.write(str(time.time()))
    f.write("server-0") #TODO
    f.write("0") #TODO
    f.write(response[0] + "\n")
    f.write(response[1] + "\n")
    f.write(response[2] + "\n")
    f.write(response[3] + "\n")
    f.write(response[4] + "\n")


async def query_server(stock_symbol, username):
    proc = Popen(['nc 192.168.4.2 4444'], stdin=PIPE, stdout=PIPE, shell=True)
    proc.stdin.write(("" + stock_symbol + " " + username + "\r").encode("utf-8"))
    output = proc.communicate()[0]
    return output.decode("utf-8")


async def process_request(stock_symbol, username):
    query_string = await query_server(stock_symbol, username)
    response = query_string.split(",")
    Cache.client.set(stock_symbol, response[0], px=60999)
    Logging.log_quote(stock_symbol, response)
    return response


async def trigger_loop(t, trigger):
    redis_client = Cache.connect()

    while True:
        triggers = redis_client.hgetall(t+'_triggers')
        for stock in triggers:
            stock = stock.decode('utf-8')

            if not redis_client.exists(stock):
                stock_price = await process_request(stock, 'fetch_server')[0]
            else:
                stock_price = redis_client.get(stock).decode('utf-8')

            stock_price = float(stock_price)

            key_prefix = stock+"_"+t
            price_key = key_prefix+'_price'
            counts = redis_client.hgetall(key_prefix+"_count")
            for user, count in counts.items():
                if count <= 0:
                    continue

                user = user.decode('utf-8')
                trigger_price = float(redis_client.hget(price_key, user).decode('utf-8'))

                trigger(redis_client, user, stock, trigger_price, stock_price)

        time.sleep(30)


async def buy_trigger(redis_client, user, stock, trigger_price, stock_price):
    if trigger_price >= stock_price:
        redis_client.xadd('command_in', {'command': 'BUY',
                                         'userID': user,
                                         'stock': stock,
                                         'value': stock_price})

        redis_client.xadd('command_in', {'command': 'COMMIT_BUY',
                                         'userID': user})


async def sell_trigger(redis_client, user, stock, trigger_price, stock_price):
    if trigger_price <= stock_price:
        redis_client.xadd('command_in', {'command': 'SELL',
                                         'userID': user,
                                         'stock': stock,
                                         'value': stock_price})

        redis_client.xadd('command_in', {'command': 'COMMIT_SELL',
                                         'userID': user})


async def main():
    try:
        Cache.client.xgroup_create('quote_in', 'fetch', 0, mkstream=True)
    except:
        pass

    threading.Thread(target=trigger_loop, args=('buy', buy_trigger))
    threading.Thread(target=trigger_loop, args=('sell', sell_trigger))

    while True:
        for _stream, messages in Cache.client.xreadgroup('fetch', Cache.container_id, {'quote_in': '>'},
                                                         1, block=30):
            print('listen to stream: ', _stream)
            for message in messages:
                #print(message, flush=True)
                stock = message[1][b'stock'].decode('utf-8')
                userid = message[1][b'userID'].decode('utf-8')
                response = await process_request(stock, userid)
                #print(response, flush=True)
                Cache.write_to_stream('quote_out', {'stock': stock, 'price': response[0]})
                Cache.client.xack('quote_in', 'tx', message[0])


Cache.client = Cache.connect()
asyncio.run(main())
