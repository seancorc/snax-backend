import json
from flask import Flask, request
from db import db, Restaurant, User, Food, Order

app = Flask(__name__)

db_filename = 'snax.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# Test.
@app.route('/api/snax/')
def snax():
    return json.dumps("snax")

# Restaurants
@app.route('/api/snax/restaurants/')
def getRestaurants():
    restaurants = Restaurant.query.all()
    get = {'success': True, 'data': [
        restaurant.serialize() for restaurant in restaurants]}
    return json.dumps(get), 200


@app.route('/api/snax/restaurant/<restaurant_name>/')
def getSpecificRestaurant(restaurant_name):
    restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
    if restaurant is not None:
        get = {'success': True, 'data': restaurant.serialize()}
        return json.dumps(get), 200
    else:
        return json.dumps({'success': False, 'error': 'Restaurant not found!'}), 404


@app.route('/api/snax/restaurant/', methods=['POST'])
def create_restaurant():
    rest_body = json.loads(request.data)
    restaurant = Restaurant(
        name=rest_body.get('name'),
    )
    db.session.add(restaurant)
    db.session.commit()
    return json.dumps({'success': True, 'data': restaurant.serialize()}), 201


@app.route('/api/snax/restaurant/<restaurant_name>/', methods=['Delete'])
def delete_restaurant(restaurant_name):
    restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
    if restaurant is not None:
        db.session.delete(restaurant)
        db.session.commit()
        return json.dumps({'success': True, 'data': restaurant.serialize()}), 201
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404


# Food
@app.route('/api/snax/restaurant/<restaurant_name>/food/')
def getFood(restaurant_name):
    restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
    if restaurant is not None:
        get = {'success': True, 'data': [
            food.serialize() for food in restaurant.food]}
        return json.dumps(get), 200
    else:
        return json.dumps({'success': False, 'error': 'Restaurant not found!'}), 404


@app.route('/api/snax/restaurant/<restaurant_name>/food/', methods=['POST'])
def create_food(restaurant_name):
    restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
    if restaurant is not None:
        body = json.loads(request.data)
        food = Food(
            name=body.get('name'),
            restaurant_id=restaurant.id,
            price=body.get('price'),
            description=body.get('description'),
            comments=body.get('comments')
        )
        restaurant.food.append(food)
        db.session.add(food)
        db.session.commit()
        return json.dumps({'success': True, 'data': food.serialize()}), 201
    return json.dumps({'success': False, 'error': 'Restaurant not found!'}), 404

@app.route('/api/snax/restaurant/food/<int:food_id>/', methods=['Delete'])
def delete_food(food_id):
    food = Food.query.filter_by(id=food_id).first()
    if food is not None:
        db.session.delete(food)
        db.session.commit()
        return json.dumps({'success': True, 'data': food.serialize()}), 201
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404

# Users
@app.route('/api/snax/users/')
def getUsers():
    users = User.query.all()
    get = {'success': True, 'data': [user.serialize() for user in users]}
    return json.dumps(get), 200


@app.route('/api/snax/user/<string:user_email>/')
def getSpecificUser(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user is not None:
        get = {'success': True, 'data': user.serialize()}
        return json.dumps(get), 200
    else:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404


@app.route('/api/snax/users/', methods=['POST'])
def create_user():
    user_body = json.loads(request.data)
    user = User(
        firstName=user_body.get('firstName'),
        lastName=user_body.get('lastName'),
        email=user_body.get('email')
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201


@app.route('/api/snax/users/<string:user_email>/', methods=['Delete'])
def delete_user(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return json.dumps({'success': True, 'data': user.serialize()}), 201
    return json.dumps({'success': False, 'error': 'User not found!'}), 404

# Orders
@app.route('/api/snax/orders/')
def getOrders():
    orders = Order.query.all()
    print([order for order in orders])
    print([order.food for order in orders])
    get = {'success': True, 'data': [order.serialize() for order in orders]}
    return json.dumps(get), 200


@app.route('/api/snax/orders/<int:order_id>/', methods=['Delete'])
def delete_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if order is not None:
        db.session.delete(order)
        db.session.commit()
        return json.dumps({'success': True, 'data': order.serialize()}), 201
    return json.dumps({'success': False, 'error': 'Order not found!'}), 404

# User Actions
@app.route('/api/snax/user/toggle_mode/<string:user_email>/', methods=['POST'])
def toggle_user_mode(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user is not None:
        user.orderer = not user.orderer
        user.deliverer = not user.deliverer
        db.session.commit()
        return json.dumps({'success': True, 'data': user.serialize()})
    return json.dumps({'success': False, 'error': 'User not found!'}), 404


@app.route('/api/snax/order/<string:user_email>/', methods=['POST'])
def create_order(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user is not None:
        neworder = Order(userID=user.id)
        for order in user.orders:
            order.mostRecent = False
        user.orders = user.orders + [neworder]
        db.session.add(neworder)
        db.session.commit()
        return json.dumps({'success': True, 'data': neworder.serialize()}), 200
    return json.dumps({'success': False, 'error': 'User not found!'}), 404


@app.route('/api/snax/placeorder/<string:user_email>/', methods=['POST'])
def place_order(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user is not None:
        if user.deliverer == True:
            return json.dumps({'success': False, 'error': 'User is in deliverer mode! Deliverers cannot place orders'}), 404
        for order in user.orders:
            if order.mostRecent:
                order.active = True
                db.session.commit()
                return json.dumps({'success': True, 'data': order.serialize()}), 201
        return json.dumps({'success': False, 'error': 'Order not found!'}), 404
    return json.dumps({'success': False, 'error': 'User not found!'}), 404


@app.route('/api/snax/fulfillorder/<int:order_id>/<string:user_email>/', methods=['POST'])
def fulfillorder(order_id, user_email):
    user = User.query.filter_by(email=user_email).first()
    if user is not None:
        if user.deliverer == False:
            return json.dumps({'success': False, 'error': 'User is in orderer mode! Orderers cannot fulfill orders'}), 404
        order = Order.query.filter_by(id=order_id).first()
        print(order.serialize())
        if order is not None:
            order.fulfillID = user.id
            order.matched = True
            db.session.commit()
            return json.dumps({'success': True, 'data': order.serialize()}), 201
        return json.dumps({'success': False, 'error': 'Order not found!'}), 404
    return json.dumps({'success': False, 'error': 'User not found!'}), 404


@app.route('/api/snax/orders/<string:user_email>/')
def getUserOrders(user_email):
    user = User.query.filter_by(email=user_email).first()
    if user is not None:
        orders = Order.query.filter_by(userID=user.id)
        serialized = [order.serialize() for order in orders]
        return json.dumps({'success': True, 'data': serialized}), 201
    return json.dumps({'success': False, 'error': 'User not found!'}), 404


@app.route('/api/snax/order/food/<int:order_id>/', methods=["POST"])
def addFoodToOrder(order_id):
    order = Order.query.filter_by(id=order_id).first()
    post_body = json.loads(request.data)
    restaurantName = post_body.get('restaurantName')
    FoodName = post_body.get('foodName')
    restaurant = Restaurant.query.filter_by(name=restaurantName).first()
    if restaurant is None:
        return json.dumps({'success': False, 'error': 'Restaurant not found!'}), 404
    food = Food.query.filter_by(
        name=FoodName, restaurant_id=restaurant.id).first()
    if order is None or food is None:
        return json.dumps({'success': False, 'error': 'Order not found!'}), 404
    order.food = order.food + [food]
    serialized = order.serialize()
    db.session.commit()
    return json.dumps({'success': True, 'data': serialized}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
