from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Many to One Food to Restaurant
#One to One Order to User
#Many to One Food to Order

association_table = db.Table('association', db.Model.metadata,
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id')))

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    food = db.relationship('Food', cascade = 'delete')
    name = db.Column(db.String, nullable=False)


    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.food = []


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
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable = False)
    orders = db.relationship("Order", secondary= association_table, back_populates = 'food')
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.String)
    comments = db.Column(db.String)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.restaurant_id =kwargs.get('restaurant_id')
        self.price = kwargs.get('price')
        self.description = kwargs.get('description','')
        self.comments = kwargs.get('comments','')
        self.orders = []

    def serialize(self):
        return{
        'id': self.id,
        'name': self.name,
        'price': self.price,
        'description': self.description,
        'comments': self.comments
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    order = db.relationship("Order", back_populates = 'user')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.order = None

    def serialize(self):
        if self.order is not None:
            return{
            'id': self.id,
            'name': self.name,
            'order': [item.serialize() for item in self.order]
            }
        else:
            return{
            'id': self.id,
            'name': self.name,
            'order': []
            }

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key = True)
    orderedid = db.Column(db.Integer, db.ForeignKey('user.id'))
    deliverid = db.Column(db.Integer, db.ForeignKey('user.id'))
    matched = db.Column(db.Boolean, nullable = False)
    active = db.Column(db.Boolean, nullable = False)
    food = db.relationship("Food", secondary= association_table, back_populates = 'order')


    def __init__(self, **kwargs):
        self.matched = False
        self.orderedid = kwargs.get('ordered_id')
        self.deliverid = None
        self.active = False
        self.food = []

    def serialize(self):
        if self.deliverUser is None:
            delivering = None
        else:
            deliveruser = User.query.filter_by(id = self.deliverid)
            delivering = deliverser.serialize()
        ordereduser = User.query.filter_by(id = self.orderedid)
        return{
        'id': self.id,
        'matched': self.matched,
        'orderer': ordereduser.serialize(),
        'placed': self.active,
        'food': [food.serialize() for food in self.food],
        'deliverer': delivering
        }
