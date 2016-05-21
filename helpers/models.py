from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


#Load data into DB for processing
Base = automap_base()
engine = create_engine('postgresql://movie:movie@localhost:5432/movieDB')
# reflect the tables
Base.prepare(engine, reflect=True)
# mapped classes are now created with names by default
# matching that of the table name.
ActedIn = Base.classes.acted_in
Actors = Base.classes.actors
Genres = Base.classes.genres
Keywords = Base.classes.keywords
Movies = Base.classes.movies
MoviesGenres = Base.classes.movies_genres
MoviesKeywords = Base.classes.movies_keywords
Series = Base.classes.series

session = Session(engine)
