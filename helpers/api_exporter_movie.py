#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models
import requests
import json


url = 'http://node0/movie/api/movie'
movies = models.session.query(models.Movies)


for movie in movies:
    # empty helpers
    series_list = []
    series_string = ''
    data = dict()

    # Query DB
    series = models.session.query(models.Series)

    # Set actor properties
    idmovie = movie.idmovies
    title = movie.title
    year = movie.year

    try:
        series = series.filter(models.Series.idmovies == idmovie).all()
        for serie in series:
            if serie.name not in series_list:
                series_list.append(str(serie.name))
        series_string = ', '.join(series_list)
    except:
        print 'skip movie ID %s' % str(idmovie)

    try:
        data['idmovie'] = idmovie
        data['name'] = str(series_string)
        data['title'] = str(title)
        data['year'] = int(year)

        response = requests.post(url, data=json.dumps(data))

        if not response.ok:
            print 'Error on adding %s' % idmovie
    except:
        print 'Error on adding %s' % idmovie

# List: ['hot dance music']
# Set: {'1973', 'blues'}
# Map: "{'2013-09-22...': 'The Fillmore', '2013-10-01....': 'The Apple Barrel'}"