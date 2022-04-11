import asyncio
import os
import time
from subprocess import Popen, PIPE, run
import Common.src.RedisStreams as RedisStreams
import threading


#redis_listener = threading.Thread(target=RedisStreams.start_listener, args=('quote_in', 'fetch', handle_stream_in,))


#RedisStreams.write_to_stream('quote_out', {'quote': RedisStreams.container_id})


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
    output = await proc.communicate()[0]
    return output.decode("utf-8")


def process_request(stock_symbol, username):
    query_string = query_server(stock_symbol, username)
    print("Response: ", query_string)
    return query_string.split(",")


async def handle_request(reader, writer):
    while True:
        data = await reader.read(100)

        print(f"Received {data}", flush=True)

        message = data.decode()
        addr = writer.get_extra_info('peername')

        #todo: log request

        print(f"Received {message!r} from {addr!r}", flush=True)

        message = message.split(',')

        if (len(message) < 2):
            writer.write(''.encode())
            await writer.drain()
            continue

        response = message[0] + ',' + process_request(message[0], message[1])
        log_request(response)

        print(f"Send: {response!r}")
        writer.write(response.encode())
        await writer.drain()

        # todo: log response


def main():

    try:
        RedisStreams.client.xgroup_create('quote_in', 'fetch', 0, mkstream=True)
    except:
        print("quote_in exists")

    while True:
        for _stream, messages in RedisStreams.client.xreadgroup('fetch', RedisStreams.container_id, {'quote_in': '>'}, 1, block=5000):
            print('listen to stream: ', _stream)
            for message in messages:
                print(message, flush=True)
                response = process_request(message[1]['userID'], message[1]['stock'])
                log_request(response)
                RedisStreams.write_to_stream('quote_out', response)
                RedisStreams.client.xack('quote_in', 'tx', message[0])


RedisStreams.client = RedisStreams.connect()
asyncio.run(main())