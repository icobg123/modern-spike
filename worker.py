import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://:p655231bba6ef045cb05d5f5f543cc41e4de3a00d309941fbc2c5264d6b8e62e4@ec2-63-34-160-32.eu-west-1.compute.amazonaws.com:13309')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()