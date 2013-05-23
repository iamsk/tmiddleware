from tornado.web import RequestHandler

from tmiddleware import TMiddleware


class TMiddlewareHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)
        # init tmiddleware
        self.tmiddleware = TMiddleware(self)

    def prepare(self):
        # add request hooks
        self.tmiddleware.request_hooks()

    def finish(self, chunk=None):
        # add before-response hooks
        self._chunk = chunk
        self.tmiddleware.before_response_hooks(self._chunk)
        RequestHandler.finish(self, self._chunk)

    def on_finish(self):
        # add after-response hooks
        self.tmiddleware.after_response_hooks()
