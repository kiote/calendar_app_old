import os
import redis


def get_connection():
    """Obtain Redis connection."""
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

    return redis.from_url(redis_url)
