import redis
import subprocess
import os


def connect():
    print("Connecting to redis")
    return redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=0)


'''Start the listener, providing stream, group, callback. The ack for messages must be handled by the callback.'''
def start_listener(stream, group, callback):
    print("Listen to ", stream, ' for group ', group)
    listener = connect()
    listener.xgroup_create(stream, group, 0, mkstream=True)

    while True:
        for _stream, messages in listener.xreadgroup(group, container_id, {stream: '>'}, 1, block=5000):
            print('listen to stream: ', _stream)
            for message in messages:
                callback(message)


def write_to_stream(stream, payload):
    print('Write ', payload, ' to ', stream, flush=True)
    global client
    client.xadd(stream, payload)


container_id = subprocess.check_output(['bash', '-c', 'cat /etc/hostname'])
client = connect()
