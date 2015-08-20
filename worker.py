from models.redis_conn import get_data_connection
from models.event_writer_structure import EventWriterStructure

def get_email(key):
    return key.split(':')[0]

redis = get_data_connection()

unchecked_keys = redis.lrange('unchecked', 0, -1)
print unchecked_keys

for key in unchecked_keys:
    event_structure = EventWriterStructure(key)
    email = event_structure.get_data_by_field_name('email')
    id = event_structure.get_data_by_field_name('event_id')
    
