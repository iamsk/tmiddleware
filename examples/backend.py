from memcache import Client


class Memcache(object):
    def __init__(self, address):
        self.conn = Client([address])

    def get(self, key):
        return self.conn.get(key)

    def set(self, key, value, timeout):
        self.conn.set(key, value, timeout)

    def delete(self, key):
        self.conn.delete(key)
