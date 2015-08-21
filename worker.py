from models.event import EventChecker
from models.redis_conn import get_data_connection

redis = get_data_connection()
unchecked_events = redis.lrange('unchecked', 0, -1)

for event in unchecked_events:
    EventChecker(event).execute()
