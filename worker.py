from rq import Worker, Queue, Connection
from models.redis_conn import get_connection

listen = ['high', 'default', 'low']

conn = get_connection

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        # burst=True mode stops worker after all jobs done
        # we need this to run workers with scheduler
        worker.work(True)
