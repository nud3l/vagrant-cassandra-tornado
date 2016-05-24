#!/usr/local/bin/python2.7
# Tornado JSON imports
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema

# Movie imports
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
        multiple = False
        query = None

        # Get arguments
        actorId = self.get_argument('actorId', None)
        firstname = self.get_argument('firstname', None)
        lastname = self.get_argument('lastname', None)

        # Check which type of input/search query is delivered and select data model to use accordingly
        # returns unique actor
        if actorId:
            query = models.ActorID.objects.filter(idactor=actorId).first()
        # returns one or multiple actors
        elif firstname and lastname:
            query = models.ActorLastFirst.objects.filter(firstname=firstname).\
                filter(lastname=lastname).all()
            multiple = True
        # returns one or multiple actors
        elif firstname:
            query = models.ActorFirst.objects.filter(firstname=firstname).all()
            multiple = True
        # returns one or multiple actors
        elif lastname:
            query = models.ActorLast.objects.filter(lastname=lastname).all()
            multiple = True

        # Retrieve details from DB
        if query and not multiple:
            actor_object['idactor'] = query.idactor
            actor_object['firstname'] = query.firstname
            actor_object['lastname'] = query.lastname
            actor_object['gender'] = query.gender
            for idmovie in query.movies_id:
                movie = dict()
                if idmovie not in movies:
                    movie['movie_id'] = idmovie
                    query_movies = models.Movie.objects.filter(idmovie=idmovie).first()
                    if query_movies:
	                    # movie['movies_name'] = query_movies.name
	                    movie['movies_title'] = query_movies.title
	                    movie['movies_year'] = query_movies.year
                    else:
                        # movie['movies_name'] = ''
                        movie['movies_title'] = ''
                        movie['movies_year'] = 1900
                    movies.append(movie)
            movies = sorted(movies, key=lambda year: year['movies_year'])
            actor_object['movie'] = movies
            actor.append(actor_object)
        elif query and multiple:
            for item in query:
            	movies = []
                actor_object = dict()
                actor_object['idactor'] = item.idactor
                actor_object['firstname'] = item.firstname
                actor_object['lastname'] = item.lastname
                actor_object['gender'] = item.gender
                for idmovie in item.movies_id:
                    movie = dict()
                    if idmovie not in movies:
                        movie['movie_id'] = idmovie
                        query_movies = models.Movie.objects.filter(idmovie=idmovie).first()
                        if query_movies:
	                        # movie['movies_name'] = query_movies.name
	                        movie['movies_title'] = query_movies.title
	                        movie['movies_year'] = query_movies.year
                        else:
                            # movie['movies_name'] = ''
                            movie['movies_title'] = ''
                            movie['movies_year'] = 1900
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
        #except:
        #    self.error('Not Found', None, 404)

    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "idactor": {"type": "integer"},
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "gender": {"type": "string"},
                "movies_id": {"type": "array"}
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
            models.ActorID.create(
                idactor=idactor,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                movies_id=movies_id
            )
            models.ActorFirst.create(
                idactor=idactor,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                movies_id=movies_id
            )
            models.ActorLast.create(
                idactor=idactor,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                movies_id=movies_id
            )
            models.ActorLastFirst.create(
                idactor=idactor,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                movies_id=movies_id
            )
            return {
                "Actor": idactor,
            }
        except:
            self.error('Error uploading', None, 500)
class Movie(APIHandler):
    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "idmovie": {"type": "integer"},
                "name": {"type": "string"},
                "title": {"type": "string"},
                "year": {"type": "integer"}
            }
        },
        output_schema={
            "type": "object",
            "properties": {
                "idmovie": {"type": "integer"}
            }
        }
    )
    def post(self):
        try:
            idmovie = self.body['idmovie']
            name = self.body['name']
            title = self.body['title']
            year = self.body['year']
            models.Movie.create(
                idmovie=idmovie,
                name=name,
                title=title,
                year=year,
            )
            return {
                "idmovie": idmovie,
            }
        except:
            self.error('Error uploading', None, 500)
