import redis
import subprocess
import os

def connect():
    return redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=0)


client = connect()
container_name = subprocess.check_output(['bash', '-c', 'echo $NAME'])


'''Start the listener, providing stream, group, callback. The ack for messages must be handled by the callback.'''
def start_listener(stream, group, callback):
    print("Listen to ", stream, ' for group ', group)
    listener = connect()
    listener.xgroup_create(stream, group, 0)

    while True:
        for _stream, messages in listener.xreadgroup(group, container_name, {stream, '>'}, 1, block=5000):
            for message in messages:
                callback(message)


def write_to_stream(stream, payload):
    print('Write ', payload, ' to ', stream)
    client.xadd(stream, payload)
