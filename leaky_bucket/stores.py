import redis
import datetime
import sqlalchemy

class DictStore(dict):

    expiration = {}

    def get(self, key: str):
        if self.expiration.get(key) and datetime.datetime.now() > self.expiration.get(key):
            self[key] = None
            self.expiration[key] = None
        return float(self.get(key) or 0.0)

    def set(self, key: str, val: float):
        if self.expiration.get(key):
            self.expiration[key] = None
        self[key] = val

    def mget(self, *keys):
        for key in keys:
            yield self.get(key)

    def mset(self, **kwargs):
        for key, val in kwargs.items():
            self.set(key, val)

    def incr(self, key: str, amount: float):
        if self.expiration.get(key) and datetime.datetime.now() > self.expiration.get(key):
            self[key] = None
            self.expiration[key] = None
        if not self.get(key):
            self[key] = amount
        else:
            self[key] += amount

    def decr(self, key: str, amount: float):
        if self.expiration.get(key) and datetime.datetime.now() > self.expiration.get(key):
            self[key] = None
            self.expiration[key] = None
        if not self.get(key):
            self[key] = amount
        else:
            self[key] -= amount

    def expire(self, key: str, time: int):
        self.expiration[key] = (datetime.datetime.now() + datetime.timedelta(seconds=time))

class RedisStore(object):

    def __init__(self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 1,
        password: str = None
    ):

        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )

    def get(self, key: str):
        return float(self.client.get(key) or 0.0)

    def set(self, key: str, val: float):
        return self.client.set(key, val)

    def mget(self,*keys):
        return (self.get(key) for key in keys)

    def mset(self, **kwargs):
        for key, val in kwargs.items():
            self.set(key, val)
    
    def incr(self, key: str, amount: float):
        return self.client.incr(key, amount)

    def decr(self, key: str, amount: float):
        return self.client.incr(key, amount)
    
    def expire(self, key: str, time: int):
        self.client.expire(key, time)

