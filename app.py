import json
from flask import Flask, request
from db import db, Restaurant, Menu, User

app = Flask(__name__)

db_filename = 'snax.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app) 
with app.app_context():
    db.create_all()

#Restaurants
@app.route('/api/snax/')
def snax():
    return json.dumps("snax")

#Restaurants
@app.route('/api/snax/restaurants/')
def getRestaurants():
    restaurants = Restaurant.query.all()
    get = {'success': True, 'data': [restaurant.serialize() for restaurant in restaurants]}
    return json.dumps(get), 200

@app.route('/api/snax/restaurant/<int:rest_id>/')
def getSpecificRestaurant(rest_id):
    restaurant = Restaurant.query.filter_by(id = rest_id).first()
    if restaurant is not None:
        get = {'success': True, 'data': restaurant.serialize()}
        return json.dumps(get), 200
    else:
        return json.dumps({'success': False, 'error': 'Restaurant not found!'}), 404

@app.route('/api/snax/restaurants/', methods = ['POST'])
def create_restaurant():
        rest_body = json.loads(request.data)
        restaurant = Restaurant(
            name = rest_body.get('name'),
            menu = rest_body.get('menu')
            )
        db.session.add(restaurant)
        db.session.commit()
        return json.dumps({'success': True, 'data': restaurant.serialize()}), 201

@app.route('/api/snax/restaurant/<int:rest_id>/', methods = ['Delete'])
def delete_restaurant(rest_id):
    restaurant = Restaurant.query.filter_by(id = rest_id).first()
    if restaurant is not None:
        db.session.delete(restaurant)
        db.session.commit()
        return json.dumps({'success': True, 'data': restaurant.serialize()}), 201
    return json.dumps({'success': False, 'error': 'Task not found!'}), 404


#Menus
@app.route('/api/snax/restaurant/<int:rest_id>/menus/')
def getMenus(rest_id):
    menus = Menu.query.filter_by(id = rest_id).first()
    if menus is not None:
        get = {'success': True, 'data': [menu.serialize() for menu in menus]}
        return json.dumps(get), 200
    else:
        return json.dumps({'success': False, 'error': 'Restaurant not found!'}), 404

@app.route('/api/snax/restaurant/<int:rest_id>/menus/', methods = ['POST'])
def create_menu(rest_id):
    restaurant = Restaurant.query.filter_by(id = rest_id).first()
    if restaurant is not None:
        body = json.loads(request.data)
        menu = Menu(
            name = body.get('name')
        )
        restaurant.menu.append(menu)
        db.session.add(menu)
        db.session.commit()
        return json.dumps({'success': True, 'data': menu.serialize()}), 201
    return json.dumps({'success': False, 'error': 'Restaurant not found!'}), 404


#Users
@app.route('/api/snax/users/')
def getUsers():
    users = User.query.all()
    get = {'success': True, 'data': [user.serialize() for user in Users]}
    return json.dumps(get), 200

@app.route('/api/snax/user/<int:user_id>/')
def getSpecificUser(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is not None:
        get = {'success': True, 'data': user.serialize()}
        return json.dumps(get), 200
    else:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404

@app.route('/api/snax/users/', methods = ['POST'])
def create_user():
    user_body = json.loads(request.data)
    user = User(
        name = user_body.get('name')
        )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201

@app.route('/api/snax/users/<int:user_id>/', methods = ['Delete'])
def delete_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return json.dumps({'success': True, 'data': user.serialize()}), 201
    return json.dumps({'success': False, 'error': 'User not found!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
