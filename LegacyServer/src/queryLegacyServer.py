import asyncio
import os
import time
from subprocess import Popen, PIPE, run
import Common.src.RedisStreams as RedisStreams
import threading


def handle_stream_in(message):
    print(message, flush=True)
    #RedisStreams.client.xack('quote', 'fetch', message.id)


redis_listener = threading.Thread(target=RedisStreams.start_listener, args=('quote_in', 'fetch', handle_stream_in,))
redis_listener.start()

RedisStreams.write_to_stream('quote_out', {'quote': RedisStreams.container_id})


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
    return query_string.split(" ")


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


async def service_loop():
    if os.environ.__contains__("FETCH_IP"):
        print(os.environ["FETCH_IP"])
        my_ip = os.environ["FETCH_IP"]
    else:
        my_ip = "127.0.0.1"

    if os.environ.__contains__("FETCH_PORT"):
        print(os.environ["FETCH_PORT"])
        my_port = os.environ["FETCH_PORT"]
    else:
        my_port = 8888

    server = await asyncio.start_server(
        handle_request, '', my_port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}', flush=True)

    async with server:
        await server.serve_forever()


asyncio.run(service_loop())


#def main():
#    stock_info = process_request("TES", "fakeUser")
#    print(stock_info)
#    print(stock_info[0])
#    print(stock_info[1])
#    print(stock_info[2])
#    print(stock_info[3])
#    print(stock_info[4])


#if __name__ == "__main__":
#    main()

