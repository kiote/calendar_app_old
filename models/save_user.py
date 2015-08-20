import os
import redis
from models.redis_conn import get_data_connection

class SaveUser:
    def __init__(self, user_info):
        self.user_info = user_info
        self.r = get_data_connection()

    def execute(self):
        count = self.get_count()
        count += 1
        self.r.set('count:' + self.user_info['email'], count)
        if count == 1:
            self.init_user_info()

    def get_count(self):
        count = self.r.get('count:' + self.user_info['email'])
        if count is None:
            count = 0
        return int(count)

    def init_user_info(self):
        self.r.set('checked:' + self.user_info['email'], 0)

    def set_changed(self):
        self.r.set('changed:' + self.user_info['email'], 1)
