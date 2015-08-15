# import os
# import redis
#
# r = redis.from_url(os.environ.get("REDIS_URL"))
# r.set('foo', 'bar')
# print r.get('foo')
from templates.event import event

print event
