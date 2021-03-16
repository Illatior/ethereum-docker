import os

from time import sleep

import pika
from redis import Redis
import psycopg2

redis = None

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
    
    
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.URLParameters('amqp://{}:{}@{}:{}/{}'.format(user, password, host, port, vhost))
    print(str(parameters))
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
    print(' [x] Received %r' % body)
    redis.set('last-block', 'asfasf')


def main():
    print('waiting to db and rmq init')
    sleep(10)

    db = setup_db()
    rmq_channel = setup_rmq()
    global redis
    redis = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)

    print('Starting listeting for blocks.')
    rmq_channel.start_consuming()

if __name__ == '__main__':
    main()
