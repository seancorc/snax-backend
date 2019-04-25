from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table('association', db.Model.metadata,
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')))

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    menu = db.relationship('Menu')
    name = db.Column(db.String, nullable=False)


    def __init__(self, **kwargs):
        #self.menu = kwargs.get('menu')
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
    restaurantID = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
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



class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cart = db.relationship("Cart", secondary = association_table, back_populates = "food")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def serialize(self):
        return{
        'id': self.id,
        'name': self.name
        }

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    food = db.relationship("Food", secondary = association_table, back_populates = "cart")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def serialize(self):
        return{
        'id': self.id,
        'name': self.name
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
