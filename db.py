from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restraunt'
    id = db.Column(db.Integer, primary_key=True)
    menu = db.relationship('Menu')
    name = db.Column(db.String, nullable=False)


    def __init__(self, **kwargs):
        self.menu = kwargs.get('menu')
        self.name = kwargs.get('name')

    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'menu': self.menu
        }

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    restaurantID = db.Column(db.Integer, db.Foreignkey('restaurant.id'))
    #db.relationship('Restraunt') Use this if we want a bidirectional many to one relationship from Menu back to Restraunt

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.restaurantID = kwargs.get('restaurantID')

    def serialize(self):
        return{
        'id': self.id,
        'name': self.name,
        'restaurantID': self.restaurantID
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def serialize(self):
        return{
        'id': self.id,
        'name': self.name
        }
