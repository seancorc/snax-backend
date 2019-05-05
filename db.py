from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Many to One Food to Restaurant
# One to One Order to User
# Many to One Food to Order

association_table = db.Table('association1', db.Model.metadata,
                             db.Column('order_id', db.Integer,
                                       db.ForeignKey('order.id')),
                             db.Column('food_id', db.Integer, db.ForeignKey('food.id')))

userorder_tabel = db.Table('association2', db.Model.metadata,
                           db.Column('order_id', db.Integer,
                                     db.ForeignKey('order.id')),
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    food = db.relationship('Food', cascade='delete')
    name = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.food = []

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'menu': [item.serialize() for item in self.food]
        }


class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurant.id'), nullable=False)
    orders = db.relationship(
        "Order", secondary=association_table, back_populates='food')
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)
    comments = db.Column(db.String)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.restaurant_id = kwargs.get('restaurant_id')
        self.price = kwargs.get('price')
        self.description = kwargs.get('description', '')
        self.comments = kwargs.get('comments', '')
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
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    orderer = db.Column(db.Boolean, nullable=False)
    deliverer = db.Column(db.Boolean, nullable=False)
    orders = db.relationship(
        "Order")

    def __init__(self, **kwargs):
        self.firstName = kwargs.get('firstName')
        self.lastName = kwargs.get('lastName')
        self.email = kwargs.get('email')
        self.orders = []
        self.orderer = True
        self.deliverer = False

    def serialize(self):
        return{
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'orders': [order.subSerialize() for order in self.orders]
        }

    def subSerialize(self):
        return{
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    matched = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    food = db.relationship(
        "Food", secondary=association_table, back_populates='orders')
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        self.matched = False
        self.active = False
        self.food = []
        self.userID = kwargs.get('userID')

    def serialize(self):
        print(self.userID)
        print('fsafdsaf')
        for f in self.food:
            if f is not None:
                print(f.serialize())

        user = User.query.filter_by(id=self.userID).first()
        user = user.subSerialize()
        otherOrderList = Order.query.filter_by(id=self.id)
        otherOrder = None
        for order in otherOrderList:
            if order != self:
                otherOrder = order
        if otherOrder is None:
            otherUser = None
        else:
            otherUser = otherOrder.user
            otherUser = otherUser.serialize()
        return{
            'id': self.id,
            'matched': self.matched,
            'user': user,
            'placed': self.active,
            'food': [food.serialize() for food in self.food],
            'otherUser': otherUser
        }

    def subSerialize(self):

        return{
            'id': self.id,
            'matched': self.matched,
            'placed': self.active,
            'food': [food.serialize() for food in self.food],
        }
