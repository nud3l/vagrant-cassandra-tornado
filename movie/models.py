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
