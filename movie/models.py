from cqlengine import columns
from cqlengine.models import Model

# Define a model
class Users(Model):
    firstname = columns.Text()
    age = columns.Integer()
    city = columns.Text()
    email = columns.Text()
    lastname = columns.Text(primary_key=True)

    def __repr__(self):
        return '%s %d' % (self.firstname, self.age)

class ActorID(Model):
    idactor = columns.Integer(primary_key=True, partition_key=True)
    firstname = columns.Text()
    lastname = columns.Text()
    gender = columns.Text()
    movies_id = columns.List(columns.Integer)
    movies_name = columns.Map(columns.Integer, columns.Text)
    movies_title = columns.Map(columns.Integer, columns.Text)
    movies_year = columns.Map(columns.Integer, columns.Integer)

class ActorLast(Model):
    idactor = columns.Integer(primary_key=True)
    firstname = columns.Text()
    lastname = columns.Text(primary_key=True, partition_key=True)
    gender = columns.Text()
    movies_id = columns.List(columns.Integer)
    movies_name = columns.Map(columns.Integer, columns.Text)
    movies_title = columns.Map(columns.Integer, columns.Text)
    movies_year = columns.Map(columns.Integer, columns.Integer)

class ActorFirst(Model):
    idactor = columns.Integer(primary_key=True)
    firstname = columns.Text(primary_key=True, partition_key=True)
    lastname = columns.Text()
    gender = columns.Text()
    movies_id = columns.List(columns.Integer)
    movies_name = columns.Map(columns.Integer, columns.Text)
    movies_title = columns.Map(columns.Integer, columns.Text)
    movies_year = columns.Map(columns.Integer, columns.Integer)

class ActorLastFirst(Model):
    idactor = columns.Integer(primary_key=True)
    firstname = columns.Text(primary_key=True, partition_key=True)
    lastname = columns.Text(primary_key=True, partition_key=True)
    gender = columns.Text()
    movies_id = columns.List(columns.Integer)
    movies_name = columns.Map(columns.Integer, columns.Text)
    movies_title = columns.Map(columns.Integer, columns.Text)
    movies_year = columns.Map(columns.Integer, columns.Integer)