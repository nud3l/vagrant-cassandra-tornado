#Python imports
import os.path
import logging.handlers

# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import options
from tornado.options import define


# Tornado JSON imports
import json
import tornado_json.application
from tornado_json.routes import get_routes


# cqlengine imports
from cqlengine import connection
from cqlengine.management import sync_table

# App imports
import movie
import models

#Custom imports
from config.Config import *
from init.Logger import *

#Setup configuration for logging
config = Config()
config.SetEnvVars(config.environment)

define("port", default=config.moviePORT, help="run on the given port", type=int)

logger = Logger(config.logLocation)
logger.info("Started movie server")

class Application(tornado_json.application.Application):
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

        routes = get_routes(movie)
        print("Routes\n======\n\n" + json.dumps(
            [(url, repr(rh)) for url, rh in routes],
            indent=2)
        )
        settings = dict(
            debug=options.debug,
            xsrf_cookies=False,
            # TODO: update manually
            cookie_secret='lpyoGs9/TAuA8IINRTRRjlgBspMDy0lKtvQNGrTnA9g=',
            )
        super(Application, self).__init__(routes=routes, generate_docs=True, settings=settings)

        # Connect to the keyspace on our cluster running at 127.0.0.1
        connection.setup(config.clusterNodes, config.clusterName)

        # Sync your model with your cql table
        sync_table(models.Users)


def main():
    tornado.options.parse_command_line()

    application = Application(logger, config)
    application.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()


