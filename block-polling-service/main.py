import os

from time import sleep
from web3 import Web3
from threading import Thread, Lock

get_blocks_timeout = os.environ['GET_BLOCKS_TIMEOUT']
send_blocks_timeout = os.environ['SEND_BLOCKS_TIMEOUT']

threads_stopped = False
threads = []
lock = Lock()

blocks_to_send = []
last_sent_block = 0

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


def get_block(w3, id='latest')
    return w3.eth.get_block(id)


def get_blocks_task(w3):
    while True:
        sleep(get_blocks_timeout)
        if threads_stopped:
            break

        last_block = get_block(w3)
        blocks_to_send.append(0, last_block)
        if int(last_block['number']) - last_sent_block > 1:
            for block_number in reversed(range(last_sent_block, int(last_block['number']))):
                blocks_to_send.append(0, get_block(w3, block_number))


def send_blocks_task(rmq):
    while True:
        sleep(send_blocks_timeout)
        if threads_stopped:
               break
               
        for block in blocks_to_send:
            converted_block = Block(block['number'], block['timestamp'])
            channel.basic_publish(exchange='e.block.forward',
                                    routing_key='r.notification.blocks',
                                    body=str(converted_block))


def exit_():
    global threads_stopped
    threads_stopped = True

def main():
    sleep(20)

    w3 = init_w3()
    print(dir(w3.eth))
    rmq = init_rmq()

    get_blocks_thread = Thread(get_blocks_task, args=[w3])
    send_blocks_thread = Thread(send_blocks_task, args=[rmq])
    threads.append(get_blocks_thread
    threads.append(send_blocks_thread)

    for thread in threads:
        threads.run()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            exit_()


if __name__ == '__main__':
    main()