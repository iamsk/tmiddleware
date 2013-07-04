import unittest
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado.options import define

from tmiddleware.handler import TMiddlewareHandler

MIDDLEWARES = ['plugins.slow_request.SlowRequestMiddleware']
define("middlewares", default=MIDDLEWARES, help="middleware class list")


class HelloWorld(TMiddlewareHandler):
    def get(self):
        import time

        time.sleep(4)
        return self.write({'hello': 'world'})


class Test(AsyncHTTPTestCase):
    def get_app(self):
        app = Application([('/', HelloWorld)])
        return app

    def test_get(self):
        request_url = '/'
        response = self.fetch(request_url)
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    testsuite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(testsuite)
