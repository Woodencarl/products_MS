import os
import redis
from rq import Worker, Queue, Connection
from api.v1.products.views import offer_updater

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker: Worker = Worker(map(Queue, listen))
        worker.work()