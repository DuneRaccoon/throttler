from .stores import *

class LeakyBucket(object):

    def __init__(self,
        key: str,
        rate: float = 1.0,
        period: float = 2.0,
        store: object = RedisStore,
        **kwargs
    ):
        self.key = key
        self.rate = rate
        self.period = period
        self.store = store(**kwargs)
