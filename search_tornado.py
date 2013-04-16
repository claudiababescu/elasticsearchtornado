import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import urllib
import json
from pyelasticsearch import *
import datetime
import time

from tornado.options import define, options

define("port", default=8010, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('http://localhost:9200/job/_search?' + \
                     urllib.urlencode({"q": query}), callback=self.on_response)

    def on_response(self, response):

        body = json.loads(response.body)
        self.get_argument('q')
        self.write(json.dumps(body))
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()