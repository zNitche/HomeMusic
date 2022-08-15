import redis
import os
import json
from home_music.app_modules.app_manager_base import AppManagerBase


class RedisManager(AppManagerBase):
    def __init__(self, db_id):
        super().__init__()

        self.server_address = os.environ.get("REDIS_SERVER_ADDRESS")
        self.server_port = int(os.environ.get("REDIS_SERVER_PORT"))
        self.db_id = db_id

        self.connection = None

        self.init_connection()

    @staticmethod
    def get_name():
        return "redis_manager"

    def init_connection(self):
        self.connection = redis.Redis(host=self.server_address, port=self.server_port, db=self.db_id)

        self.connection.flushdb()

    def set_value(self, key, value):
        self.connection.set(key, json.dumps(value))

    def get_value(self, key):
        value = None

        data = self.connection.get(key)

        if data:
            value = json.loads(data)

        return value
