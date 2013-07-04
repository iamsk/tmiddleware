import tornado
import tornado.httpserver
from tornado.options import define, options

from tmiddleware.handler import TMiddlewareHandler

define('port', 7777)
MIDDLEWARES = ['plugins.slow_request.SlowRequestMiddleware',
               'plugins.profile.ProfileMiddleware']
define("middlewares", default=MIDDLEWARES, help="middleware class list")


class With(TMiddlewareHandler):
    def get(self):
        import time

        time.sleep(4)
        return self.finish('Hello World!')


def run():
    application = tornado.web.Application([('/', With)])
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()
