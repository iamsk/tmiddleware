# -*- coding: utf-8 -*-

import pstats
import cProfile
import functools
from cStringIO import StringIO
import json


class ProfileMiddleware(object):
    def __init__(self, handler):
        self.handler = handler
        self.profile = cProfile.Profile()
        need_profile = self.handler.get_argument("__profile__", None)
        self._sort = list(self.handler.get_argument("__sort__", "cumulative,calls,time").split(','))
        self._limit = int(self.handler.get_argument("__limit__", 20))
        self._enabled_profile = True if need_profile else False

    def request_hook(self):
        if not self._enabled_profile:
            return
        self.stream_buffer = StringIO()
        self.profile = cProfile.Profile()
        if hasattr(self.handler, 'get'):
            self.handler.get = functools.partial(self.profile.runcall, self.handler.get)
        elif hasattr(self.handler, 'post'):
            self.handler.post = functools.partial(self.profile.runcall, self.handler.post)
        elif hasattr(self.handler, 'put'):
            self.handler.put = functools.partial(self.profile.runcall, self.handler.put)
        elif hasattr(self.handler, 'delete'):
            self.handler.delete = functools.partial(self.profile.runcall, self.handler.delete)

    def before_response_hook(self, chunk):
        if not self._enabled_profile:
            return
        if not chunk:
            return
        profile_string = StringIO()
        stats = pstats.Stats(self.profile, stream=profile_string)
        stats.strip_dirs()
        stats.sort_stats(*self._sort).print_stats(self._limit)
        _ret = profile_string.getvalue()
        try:
            temp = json.loads(chunk)
            temp['__profile__'] = _ret
            chunk = json.dumps(temp)
        except Exception:
            _ret = "<pre>%s</pre>" % _ret
            if "</body>" in chunk:
                pos = chunk.rindex('</body>')
                chunk = chunk[:pos] + _ret + chunk[pos:]
            else:
                chunk = '<html><body><div>%s<div><div>%s</div></body></html>' % (chunk, _ret)
        self.handler._chunk = chunk
