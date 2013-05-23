# -*- coding: utf-8 -*-

import time
from datetime import datetime
from tornado.options import options


class SlowRequestMiddleware(object):
    def __init__(self, handler):
        self.handler = handler

    def request_hook(self):
        self.request_time = datetime.now()
        self.start_time = int(time.time())

    def after_response_hook(self):
        end_time = int(time.time())
        cost_time = end_time - self.start_time
        if cost_time > getattr(options, 'slow_request_time', 3):
            print '-----------------------------------Slow Request---------------------------------'
            print '-> Request time : ', self.request_time
            print '-> Current url : ', self.handler.request.uri
            print '-> Cost time : ', cost_time, 's'
            print '--------------------------------------------------------------------------------'
