from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Many to Many Cart to food
#Many to One Food to Restaurant
#One to One Cart to User
#One to One Cart to Order ------Only want to add after complete?

association_table = db.Table('association', db.Model.metadata,
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')))

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    food = db.relationship('Food', cascade = 'delete')
    name = db.Column(db.String, nullable=False)


    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'menu': [food.serialize() for item in self.food]
        }

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cart = db.relationship("Cart", secondary = association_table, back_populates = "food")
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.String)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.restaurant_id =kwargs.get('restaurant_id')
        self.price = kwargs.get('price')
        self.description = kwargs.get('description')

    def serialize(self):
        return{
        'id': self.id,
        'name': self.name,
        'price': self.price,
        'description': self.description
        }

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    food = db.relationship("Food", secondary = association_table, back_populates = "cart")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.food = None
        self.user_id = kwargs.get('user_id')


    def serialize(self):
        return{
        'id': self.id,
        'name': self.name,
        'food': self.food,
        'user': self.user
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    cart = db.relationship("Cart", uselist = False, back_populates = 'user')
    order = db.relationship("Order", uselist = False, back_populates = 'user')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.cart = None
        self.order = None

    def serialize(self):
        return{
        'id': self.id,
        'name': self.name,
        'cart': [item.serialize() for item in self.cart]
        }

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key = True)
    orderedUser = db.relationship("User", back_populates = 'order')
    deliverUser = db.relationship("User", back_populates = 'order')
    matched = db.Column(db.Boolean, nullable = False)


    def __init__(self, **kwargs):
        self.matched = kwargs.get('matched', False)
        self.orderedUser = None
        self.deliverUser = None

    def serialize(self):
        return{
        'id': self.id,
        'matched': self.matched,
        'orderer': self.orderedUser.serialize()
        }
