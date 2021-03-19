import os
import pika
import threading

from time import sleep
from web3 import Web3

get_blocks_timeout = int(os.environ['GET_BLOCKS_TIMEOUT'])
send_blocks_timeout = int(os.environ['SEND_BLOCKS_TIMEOUT'])

threads_stopped = False
threads = []
lock = threading.Lock()

blocks_to_send = []
last_sent_block = -1


class Block:
    def __init__(self, number, time):
        self.block_number = number
        self.block_time = time

    def __str__(self):
        return '{}, {}'.format(self.block_number, self.block_time)


def init_w3():
    provider = Web3.HTTPProvider(
        'http://{}:{}'.format(
            os.environ['NODE_HOST'],
            os.environ['NODE_RPC_PORT']
        )
    )
    return Web3(provider)


def init_rmq():
    user = os.environ['RMQ_USER']
    password = os.environ['RMQ_PASSWORD']

    host = os.environ['RMQ_HOST']
    port = os.environ['RMQ_PORT']
    vhost = os.environ['RMQ_VHOST']
    if vhost == '/':
        vhost = ''

    parameters = pika.URLParameters('amqp://{}:{}@{}:{}/{}'.format(user, password, host, port, vhost))

    rmq_connection = pika.BlockingConnection(parameters)
    channel = rmq_connection.channel()

    return channel


def get_block(w3, block_id='latest'):
    return w3.eth.getBlock(block_id)


def get_blocks_task(w3):
    global last_sent_block, blocks_to_send
    while True:
        sleep(get_blocks_timeout)
        if threads_stopped:
            break

        last_block = get_block(w3)
        print('last block - {}\nlast send block - {}\n\n'.format(last_block['number'], last_sent_block))
        if int(last_block['number']) - last_sent_block == 1:
            blocks_to_send.insert(0, last_block)
        elif int(last_block['number']) - last_sent_block > 1:
            for block_number in range(last_sent_block, int(last_block['number'])):
                if block_number < 0:
                    continue

                blocks_to_send.insert(0, w3.eth.get_block(block_number))


def send_blocks_task(channel):
    global last_sent_block, blocks_to_send, lock
    while True:
        sleep(send_blocks_timeout)
        if threads_stopped:
            break

        lock.acquire()
        for block in blocks_to_send:
            converted_block = Block(block['number'], block['timestamp'])
            channel.basic_publish(exchange='e.block.forward',
                                  routing_key='r.notification.blocks',
                                  body=str(converted_block))

        if len(blocks_to_send) > 0:
            last_sent_block = blocks_to_send[-1]['number']
            blocks_to_send = []

        lock.release()


def exit_():
    global threads_stopped
    threads_stopped = True


def main():
    w3 = init_w3()
    rmq = init_rmq()

    print('Init completed. Starting threads')

    get_blocks_thread = threading.Thread(target=get_blocks_task, args=[w3])
    threads.append(get_blocks_thread)
    send_blocks_thread = threading.Thread(target=send_blocks_task, args=[rmq])
    threads.append(send_blocks_thread)

    for thread in threads:
        thread.start()
    print('Threads started')

    try:
        while True:
            pass
    except KeyboardInterrupt:
        exit_()


if __name__ == '__main__':
    main()
