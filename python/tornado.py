#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import textwrap

from tornado.options import define, options
define("port", default=8000, help="run on given port", type=int)

class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user.')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/reverse/(\w+)", ReverseHandler),
        (r"/wrap", WrapHandler),
        (r"/", IndexHandler)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
