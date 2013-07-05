#-*- coding: utf-8 -*-

import logging
from tornado.options import options


class TMiddleware():
    def __init__(self, handler):
        self.handler = handler
        self.request_middlewares = []
        self.before_response_middlewares = []
        self.after_response_middlewares = []
        self.init()

    def init(self):
        if hasattr(options, 'middlewares') and len(options.middlewares) > 0:
            for mclass in options.middlewares:
                modname, clsname = self._split_name(mclass)
                try:
                    mod = __import__(modname, globals(), locals(), [clsname])
                except ImportError, e:
                    logging.error("module __import__ failed: {0}".format(e), exc_info=True)
                    continue
                try:
                    cls = getattr(mod, clsname)
                    inst = cls(self.handler)
                    if hasattr(inst, 'request_hook'):
                        self.request_middlewares.append(inst)
                    if hasattr(inst, 'before_response_hook'):
                        self.before_response_middlewares.append(inst)
                    if hasattr(inst, 'after_response_hook'):
                        self.after_response_middlewares.append(inst)
                except AttributeError, e:
                    logging.error("cant instantiate cls: {0}".format(e), exc_info=True)
                    print "cant instantiate cls", e

    def _run_hooks(self, type, middlewares, chunk=None):
        for middleware in middlewares:
            try:
                if type == 'request':
                    middleware.request_hook()
                if type == 'before_response':
                    middleware.before_response_hook(chunk)
                if type == 'after_response':
                    middleware.after_response_hook()
            except Exception as e:
                logging.error(e, exc_info=True)

    def request_hooks(self):
        """
        Executed in prepare() of the Request, as before http method
        """
        self._run_hooks('request', self.request_middlewares)

    def before_response_hooks(self, chunk=None):
        """
        Executed in finish() of the Request, as after http method
        """
        self._run_hooks('before_response', self.before_response_middlewares, chunk)

    def after_response_hooks(self):
        """
        Executed in on_finish(), as after finish() of the Request
        Useful for logging
        """
        self._run_hooks('after_response', self.after_response_middlewares)

    def _split_name(self, path):
        try:
            pos = path.rindex('.')
        except ValueError:
            raise Exception('%s is invalid' % path)
        return path[:pos], path[pos + 1:]
