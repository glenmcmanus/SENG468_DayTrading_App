import asyncio
import os
from subprocess import Popen, PIPE, run

#This code is incomplete

#TODO:
#receive input from transaction server
#reformat ouput in some way
#send output to transaction server (possibly a different file)

async def query_server(stock_symbol, username):
    proc = Popen(['nc 192.168.4.2 4444'], stdin=PIPE, stdout=PIPE, shell=True)
    proc.stdin.write(("" + stock_symbol + " " + username + "\r").encode("utf-8"))
    output = await proc.communicate()[0]
    return output.decode("utf-8")

def process_request(stock_symbol, username):
    query_string = query_server(stock_symbol, username)
    return query_string.split(",")

def main():
    stock_info = process_request("TES", "fakeUser")
    print(stock_info)
    print(stock_info[0])
    print(stock_info[1])
    print(stock_info[2])
    print(stock_info[3])
    print(stock_info[4])

async def handle_request(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    #todo: log request

    print(f"Received {message!r} from {addr!r}")

    message = message.split(',')

    response = process_request(message[0], message[1])

    print(f"Send: {response!r}")
    writer.write(response.encode())
    await writer.drain()

    # todo: log response

    print("Close the connection")
    writer.close()

def service_loop():
    if os.environ.__contains__("FETCH_IP"):
        print(os.environ["FETCH_IP"])
        my_ip = os.environ["FETCH_IP"]
    else:
        my_ip = "127.0.0.1"

    if os.environ.__contains__("FETCH_PORT"):
        print(os.environ["FETCH_PORT"])
        my_port = os.environ["FETCH_PORT"]
    else:
        my_port = 8889

    server = await asyncio.start_server(
        handle_request, my_ip, my_port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}', flush=True)

    async with server:
        await server.serve_forever()

asyncio.run(service_loop())

if __name__ == "__main__":
    main()
