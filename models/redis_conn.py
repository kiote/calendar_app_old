import os
import redis


def get_data_connection():
    """Obtain Redis connection for data storing."""
    return redis.from_url(os.getenv('REDIS_URL'))
