#-*- coding: utf-8 -*-

class Memcache(object):
    """
    address=127.0.0.1:11211
    # TODO 链接断开后没有自动重连机制
    """
    def __init__(self, address):
        from memcache import Client

        self.conn = Client([address])

    def get(self, key):
        return self.conn.get(key)

    def set(self, key, value, timeout):
        self.conn.set(key, value, timeout)

    def delete(self, key):
        self.conn.delete(key)


class Redis(object):
    """
    address=['1270.0.1', 6379, 0]
    """
    def __init__(self, address):
        from redis import Redis

        self.conn = Redis(host=address[0], port=address[1], db=address[2])

    def get(self, key):
        return self.conn.get(key)

    def set(self, key, value, timeout):
        self.conn.set(key, value)
        self.conn.expire(key, timeout)

    def delete(self, key):
        self.conn.delete(key)
