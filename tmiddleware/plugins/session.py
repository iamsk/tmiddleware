# -*- coding: utf-8 -*-

import os
import json
from tornado.options import options


class Session(object):
    def _generate_sid(self):
        sid = os.urandom(32).encode('hex')  # 256 bits of entropy
        return sid

    def _get_session(self, sid):
        if not sid:
            session = {'id': self._generate_sid()}
            return session

        data = self.backend.get(sid)
        if not data:
            session = {'id': self._generate_sid()}
        else:
            session = json.loads(data)
        return session

    def _set_session(self, sid, value):
        sid = str(sid)  # type(sid) is unicode
        self.backend.set(sid, json.dumps(value), options.session_timeout)

    def del_session(self, sid, value):
        self.backend.delete(sid)


class SessionMiddleware(Session):
    def __init__(self, handler):
        self.handler = handler
        self.backend = self.handler.application.backend

    def request_hook(self):
        self.sid = self.handler.get_secure_cookie('sid', None)
        self.handler.session = self._get_session(self.sid)

    def after_response_hook(self):
        if not self.sid:
            self.handler.set_secure_cookie('sid', self.handler.session['id'])
        self._set_session(self.handler.session['id'], self.handler.session)
