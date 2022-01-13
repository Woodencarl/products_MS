from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from api.v1.products.views import offer_updater
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

scheduler = BlockingScheduler()

q = Queue(connection=conn)


def update_offers():
    q.enqueue(offer_updater)


scheduler.add_job(update_offers)  # enqueue right away once
scheduler.add_job(update_offers, 'interval', minutes=1)
scheduler.start()
