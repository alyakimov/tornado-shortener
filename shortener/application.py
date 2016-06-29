#!/usr/bin/env python
"""
Runnable Applicatin
Igor Alyakimov ialyakimov@me.com
"""
from __future__ import absolute_import, division, print_function, with_statement

import os
import sys
sys.path.append(os.getcwd())
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.httpclient
import shortener.settings
from tornado.options import options
from shortener.handlers import main


def create_app(settings):
    """ Create application routing """
    return tornado.web.Application([
        tornado.web.url(r"/", main.MainHandler, name="home"),
        tornado.web.url(r"/_", main.ApiHandler, name="api"),
        tornado.web.url(r"/([A-Za-z0-9]+)\+", main.InfoHandler, name="info"),
        tornado.web.url(r"/([A-Za-z0-9]+)", main.ApiHandler, name="redirect"),

        # 404 handler
        tornado.web.url(r"/(.*)", main.NotFoundHandler),
    ], **settings)


if __name__ == "__main__":

    tornado.options.parse_command_line()

    application = create_app({
        "debug": options.tornado_debug,
        "cookie_secret": options.cookie_secret,
        "template_path": options.template_path,
        "autoreload": False
    })

    server = tornado.httpserver.HTTPServer(application)
    server.bind(options.tornado_port)
    # Forks multiple sub-processes
    server.start(1)
    tornado.ioloop.IOLoop.instance().start()