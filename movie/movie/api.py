#!/usr/local/bin/python2.7
# Tornado JSON imports
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
import json
import datetime

# Categories imports
from movie import models

# Custom handlers
class User(APIHandler):
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "User": {"type": "string"},
            }
        }
    )
    def get(self):
        try:
            models.Users.create(firstname='Bob', age=35, city='Austin', email='bob@example.com', lastname='Jones')
            q = models.Users.get(lastname='Jones')
            return {
                "User": str(q),
            }
        except:
            self.set_status(404, 'No account available')

class Actor(APIHandler):
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "Actor": {"type": "array"},
            }
        }
    )
    def get(self):
        # try:
        movies = []
        actor = []
        actor_object = dict()
        actorId = self.get_argument('actorId', None)
        firstname = self.get_argument('firstname', None)
        lastname = self.get_argument('lastname', None)
        # returns unique actor
        if actorId:
            query = models.ActorID.objects.filter(idactor=actorId).first()
            if query:
                actor_object['idactor'] = query.idactor
                actor_object['firstname'] = query.firstname
                actor_object['lastname'] = query.lastname
                actor_object['gender'] = query.gender
                for q in query.movies_id:
                    movie = dict()
                    if q not in movies:
                        movie['movie_id'] = q
                        movie['movies_name'] = query.movies_name[q]
                        movie['movies_title'] = query.movies_title[q]
                        movie['movies_year'] = query.movies_year[q]
                        movies.append(movie)
                movies = sorted(movies, key=lambda year: year['movies_year'])
                actor_object['movie'] = movies
                actor.append(actor_object)
        # returns one or multiple actors
        elif firstname and lastname:
            query = models.ActorLastFirst.objects.filter(firstname=firstname).\
                filter(lastname=lastname).all()
            for item in query:
                actor_object = dict()
                actor_object['idactor'] = item.idactor
                actor_object['firstname'] = item.firstname
                actor_object['lastname'] = item.lastname
                actor_object['gender'] = item.gender
                for q in item.movies_id:
                    movie = dict()
                    if q not in movies:
                        movie['movie_id'] = q
                        movie['movies_name'] = item.movies_name[q]
                        movie['movies_title'] = item.movies_title[q]
                        movie['movies_year'] = item.movies_year[q]
                        movies.append(movie)
                movies = sorted(movies, key=lambda year: year['movies_year'])
                actor_object['movie'] = movies
                actor.append(actor_object)
        # returns one or multiple actors
        elif firstname:
            query = models.ActorFirst.objects.filter(firstname=firstname).all()
            for item in query:
                actor_object = dict()
                actor_object['idactor'] = item.idactor
                actor_object['firstname'] = item.firstname
                actor_object['lastname'] = item.lastname
                actor_object['gender'] = item.gender
                for q in item.movies_id:
                    movie = dict()
                    if q not in movies:
                        movie['movie_id'] = q
                        movie['movies_name'] = item.movies_name[q]
                        movie['movies_title'] = item.movies_title[q]
                        movie['movies_year'] = item.movies_year[q]
                        movies.append(movie)
                movies = sorted(movies, key=lambda year: year['movies_year'])
                actor_object['movie'] = movies
                actor.append(actor_object)
        # returns one or multiple actors
        elif lastname:
            query = models.ActorLast.objects.filter(lastname=lastname).all()
            for item in query:
                actor_object = dict()
                actor_object['idactor'] = item.idactor
                actor_object['firstname'] = item.firstname
                actor_object['lastname'] = item.lastname
                actor_object['gender'] = item.gender
                for q in item.movies_id:
                    movie = dict()
                    if q not in movies:
                        movie['movie_id'] = q
                        movie['movies_name'] = item.movies_name[q]
                        movie['movies_title'] = item.movies_title[q]
                        movie['movies_year'] = item.movies_year[q]
                        movies.append(movie)
                movies = sorted(movies, key=lambda year: year['movies_year'])
                actor_object['movie'] = movies
                actor.append(actor_object)
        if actor:
            return {
                "Actor": actor,
            }
        else:
            self.error('Not Found', None, 404)
        # except:
        #    self.error('Not Found', None, 404)
    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "idactor": {"type": "integer"},
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "gender": {"type": "string"},
                "movies_id": {"type": "array"},
                "movies_name": {"type": "object"},
                "movies_title": {"type": "object"},
                "movies_year": {"type": "object"},
            }
        },
        output_schema={
            "type": "object",
            "properties": {
                "idactor": {"type": "integer"},
            }
        }
    )
    def post(self):
        try:
            idactor = self.body['idactor']
            firstname = self.body['firstname']
            lastname = self.body['lastname']
            gender = self.body['gender']
            movies_id = self.body['movies_id']
            movies_name = self.body['movies_name']
            movies_title = self.body['movies_title']
            movies_year = self.body['movies_year']
            models.ActorID.create(
                idactor=idactor,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                movies_id=movies_id,
                movies_name=movies_name,
                movies_title=movies_title,
                movies_year=movies_year
            )
            models.ActorFirst.create(
                idactor=idactor,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                movies_id=movies_id,
                movies_name=movies_name,
                movies_title=movies_title,
                movies_year=movies_year
            )
            models.ActorLast.create(
                idactor=idactor,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                movies_id=movies_id,
                movies_name=movies_name,
                movies_title=movies_title,
                movies_year=movies_year
            )
            models.ActorLastFirst.create(
                idactor=idactor,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                movies_id=movies_id,
                movies_name=movies_name,
                movies_title=movies_title,
                movies_year=movies_year
            )
            return {
                "User": idactor,
            }
        except:
            self.error('Error uploading', None, 500)