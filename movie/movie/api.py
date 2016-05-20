#!/usr/local/bin/python2.7
# Tornado JSON imports
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
import json
import datetime
import sqlalchemy

# Categories imports
from movie import models

class BaseHandler(APIHandler):
    @property
    def db(self):
        return self.application.db

# Custom handlers
class Movie(BaseHandler):
    #@schema.validate(
    #    output_schema={
    #        "type": "object",
    #        "properties": {
    #            "transaction": {"type": "array"},
    #        }
    #    }
    #)
    def get(self):
        try:
            models.Users.create(firstname='Bob', age=35, city='Austin', email='bob@example.com', lastname='Jones')
            q = models.Users.get(lastname='Jones')
            return {
                "User": q,
            }
        except:
            self.set_status(404, 'No account available')