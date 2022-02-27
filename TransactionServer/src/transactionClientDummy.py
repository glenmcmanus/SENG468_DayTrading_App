import asyncio
import src.Common.Constants as Const

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    message = message.split(',', 1)

    message[0] = str(Const.TRANSACTION_STR_TO_BYTE[message[0]])

    message = ",".join(message)

    print(f'ENCODE: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client("ADD,oY01WVirLr,63511.53"))