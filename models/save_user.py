import redis

class SaveUser:
    def __init__(self, user):
        self.user = user
        self.r = redis.from_url(os.environ.get("REDIS_URL"))

    def execute(self):
        count = self.get_count()
        count += 1
        self.r.set(self.user['email'] + ':count', count)

    def get_count(self):
        count = self.r.get(self.user['email'] + ':count')
        if count is None:
            count = 0
        return count
