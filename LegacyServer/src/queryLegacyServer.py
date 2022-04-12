import asyncio
import os
import time
from subprocess import Popen, PIPE, run
import Common.src.Cache as RedisStreams
import Common.src.Constants as Const

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
    print("Response: ", query_string)
    return query_string.split(",")


async def main():

    try:
        RedisStreams.client.xgroup_create('quote_in', 'fetch', 0, mkstream=True)
    except:
        print("quote_in exists")

    while True:
        for _stream, messages in RedisStreams.client.xreadgroup('fetch', RedisStreams.container_id, {'quote_in': '>'}, 1, block=5000):
            print('listen to stream: ', _stream)
            for message in messages:
                print(message, flush=True)
                response = await process_request(message[1][b'userID'].decode('utf-8'), message[1][b'stock'].decode('utf-8'))
                print(response, flush=True)
                log_request(response)
                RedisStreams.client.set(response[1], response[0], px=60999)
                RedisStreams.write_to_stream('quote_out', {'stock': response[1], 'price': response[0]})
                RedisStreams.client.xack('quote_in', 'tx', message[0])


RedisStreams.client = RedisStreams.connect()
asyncio.run(main())
