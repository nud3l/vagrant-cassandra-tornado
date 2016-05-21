#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models
import csv

actors = models.session.query(models.Actors)
for actor in actors:
    # empty helpers
    movies_id = []
    movies_name = dict()
    movies_title = dict()
    movies_year = dict()
    series_list = []
    series_string = ''
    data = []

    # Query DB
    movies = models.session.query(models.Movies)
    acted_in = models.session.query(models.ActedIn)
    series = models.session.query(models.Series)

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
                movies_title[movie.idmovies] = str(movie.title).replace("'", '').replace("/", '+').replace('"', '')
                if movie.year:
                    movies_year[movie.idmovies] = movie.year
                else:
                    movies_year[movie.idmovies] = 0
                series = series.filter(models.Series.idmovies == movie.idmovies)
                for serie in series:
                    if serie.name not in series_list:
                        series_list.append(str(serie.name).replace("'", '').replace("/", '+').replace('"', ''))
                series_string = ', '.join(series_list)
                movies_name[movie.idmovies] = str(series_string)
    except:
        print 'skip actor ID %s' % str(idactor)

    with open('csv_export_actors_large.csv', 'wb') as csvfile:
        cqlwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data.append(idactor)
        data.append(firstname)
        data.append(lastname)
        data.append(gender)
        data.append(movies_id)
        data.append(movies_name)
        data.append(movies_title)
        data.append(movies_year)
        cqlwriter.writerow(data)

# List: ['hot dance music']
# Set: {'1973', 'blues'}
# Map: "{'2013-09-22...': 'The Fillmore', '2013-10-01....': 'The Apple Barrel'}"