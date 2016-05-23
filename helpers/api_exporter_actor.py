#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models
import requests
import json

url = 'http://node0/movie/api/actor'
actors = models.session.query(models.Actors)

for actor in actors:
    # empty helpers
    movies_id = []
    data = dict()

    # Query DB
    movies = models.session.query(models.Movies)
    acted_in = models.session.query(models.ActedIn)

    # Set actor properties
    idactor = actor.idactors
    firstname = actor.fname
    lastname = actor.lname
    gender = actor.gender

    # Filter where acted in
    acted_in = acted_in.filter(models.ActedIn.idactors == idactor)

    try:
        for acted in acted_in:
            movie = movies.filter(models.Movies.idmovies == acted.idmovies).first()
            if movie.idmovies not in movies_id:
                movies_id.append(movie.idmovies)
    except:
        print 'skip actor ID %s' % str(idactor)

    try:
        data['idactor'] = idactor
        data['firstname'] = str(firstname)
        data['lastname'] = str(lastname)
        data['gender'] = str(gender)
        data['movies_id'] = movies_id

        response = requests.post(url, data=json.dumps(data))

        if not response.ok:
            print 'Error on adding %s' % idactor
    except:
        print 'Error on adding %s' % idactor

# List: ['hot dance music']
# Set: {'1973', 'blues'}
# Map: "{'2013-09-22...': 'The Fillmore', '2013-10-01....': 'The Apple Barrel'}"