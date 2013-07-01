import json

import tornado
import tornado.httpserver
from tornado.options import define, options

from tmiddleware.handler import TMiddlewareHandler
import backend

define('port', 7777)
MIDDLEWARES = ['plugins.session.SessionMiddleware']
define("middlewares", default=MIDDLEWARES, help="middleware class list")

define('session_timeout', 3600)


class With(TMiddlewareHandler):
    def get(self):
        self.set_secure_cookie('sid', self.session['id'])
        self.session['hello'] = 'world!'
        return self.finish(json.dumps(self.session))

settings = {
    'cookie_secret': '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
}


def run():
    application = tornado.web.Application([('/', With)], **settings)
    application.backend = backend.Memcache('127.0.0.1:11211')
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    run()
