import os
import json

from time import sleep

import pika
import psycopg2

from redis import Redis

redis = None
db = None


class Block:
    def __init__(self, number, time):
        self.block_number = number
        self.block_time = time

    def __str__(self):
        return '{}, {}'.format(self.block_number, self.block_time)


def setup_redis():
    redis =  Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)

    if not redis.get('nonce'):
        redis.set('nonce', 0)

    return redis

def setup_db():
    database = os.environ['DB_NAME']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    host = os.environ['DB_HOST']

    db_connection = psycopg2.connect(dbname=database, user=user, 
                        password=password, host=host)

    print('Successfully connected to db.')

    return db_connection


def setup_rmq():
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

    channel.basic_consume(
        queue='q.test-consumer.blocks',
        on_message_callback=block_received_callback,
        auto_ack=True
    )

    print('Successfully connected to rmq and registered consumer.')
    return channel


def block_received_callback(ch, method, properties, body):
    message = body.decode('utf-8')    
    print(' [x] Received %r' % message)

    block = None
    try:
        json_message = json.loads(message)
        block = Block(json_message['block_id'], json_message['block_time'])
    except Exception as e:
        print(str(e))
        return 

    write_block_to_db(block)
    redis.set('nonce', int(redis.get('nonce')) + 1)


def write_block_to_db(block: Block):
    with db.cursor() as cursor:
        db.autocommit = True
        sql = '''
            INSERT INTO
                blocks(block_id, block_time)
            VALUES
                ({})
            '''.format(str(block))

        cursor.execute(sql)


def main():
    print('waiting to db and rmq init')
    sleep(10)

    global redis, db
    db = setup_db()
    rmq_channel = setup_rmq()
    redis = setup_redis()

    print('Starting listeting for blocks.')
    rmq_channel.start_consuming()

if __name__ == '__main__':
    main()
