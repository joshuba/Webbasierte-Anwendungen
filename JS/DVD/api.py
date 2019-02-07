from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from models import *
from database import db
from sqlalchemy import func, cast
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus
from math import ceil
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/products', methods=['PUT'])
@jwt_required
def put_take_item():
    try:
        data = request.json
        inv = Inventory.query.filter_by(prod_id=data['id']).one()
        if data['type'] == 'add':
            inv.quan_in_stock += int(data['quantity'])
            db.session.commit()
        elif inv.quan_in_stock > 0:
            inv.quan_in_stock -= int(data['quantity'])
            db.session.commit()
        else:
            return jsonify({'status': 'error'})
        return jsonify({'status': 'success'})
    except SQLAlchemyError as err:
        return jsonify({'status': 'error'})
        raise err


# @api.route('/search/')
# def advanced_search(lookingfor):
#     search = request.json
#     if search['type'] == "user":
#         q = User.query
#     elif search['type'] == "product":
#         q = Product.query
#         for key, value in search['fields'].iteritems():
#     elif search['type'] == "order":
#         q = Order.query
#
#     for key, value in search['fields'].iteritems():
#         if value['comparator'] == '>':
#             q = users.filter(getattr(User, key) > value['val'])
#         elif value['comparator'] == '<':
#             q = users.filter(getattr(User, key) < value['val'])
#         elif value['comparator'] == '=':
#             q = users.filter(getattr(User, key) == value['val'])
#         elif value['comparator'] == 'in':
#             q = users.filter(cast(getattr(User, key), db.String).contains(value['val']))
#     return jsonify(results=[i._asdict() for i in q.all()], type=search['type'])
#     else:
#         return jsonify({'status': 'No fucking clue how you got here.'})



@api.route('/products', defaults={'page': 1, 'perpage': 20, 'productid': -1}, methods=['GET'])
@api.route('/products/<int:productid>', defaults={'page': -1, 'perpage': -1}, methods=['GET'])
@api.route('/products/<int:page>/<int:perpage>', defaults={'productid': -1}, methods=['GET'])
@jwt_required
def products(page, perpage, productid):
    sortParam = ""
    if request.args.get('sort'):
        sortParam = request.args.get('sort').replace("_", " ",)
    if request.args.get('s'):
        searchVar = request.args.get('s')
        products = Product.query.filter(
         func.lower(cast(Product.id, db.String)).contains(searchVar.lower()) |
         func.lower(cast(Product.category, db.String)).contains(searchVar.lower()) |
         func.lower(cast(Product.title, db.String)).contains(searchVar.lower()) |
         func.lower(cast(Product.actor, db.String)).contains(searchVar.lower())).order_by(sortParam)
        return jsonify(products=[p._asdict() for p in products.all()])
    elif productid != -1:
        product = Product.query.filter_by(id=productid).join(Inventory, Product.id == Inventory.prod_id, aliased=True).one()
        print(product._asdict())
        return jsonify(product=product._asdict())
    else:
        page, lastpage = correctPage(page, Product.query.count(), perpage)
        products = Product.query.order_by(sortParam).paginate(per_page=perpage, page=page).items
        return jsonify(products=[o._asdict() for o in products], numpages=ceil(lastpage))


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Customer.query.filter_by(**data).one()
    if user is None:
        return jsonify({"msg": "Wrong User or Password"}), 400
    access_token = create_access_token(identity=data['username'])
    return jsonify(access_token=access_token), 200


@api.route('/orders', methods=['POST'])
def addOrder():
    order_json = request.json
    cust = Customer.query.filter_by(username=order_json['username']).one()
    total = float(order_json['total'])
    date = datetime.now()
    newOrder = Order(
     orderdate=date,
     customer=cust,
     netamount=total / 1.07,
     tax=total * 0.07,
     totalamount=total
    )
    db.session.flush()
    try:
        db.session.add(newOrder)
        db.session.commit()
        lines = []
        for (num, item) in enumerate(order_json['items']):
            newLine = Orderline(
             orderlineid=num,
             orderid= newOrder.id,
             prod_id=item['id'],
             quantity=item['qty'],
             orderdate=newOrder.orderdate
            )
            lines.append(newLine)
        db.session.add_all(lines)
        db.session.commit()
        return jsonify({'orderid': newOrder.id, 'status': 'success'})
    except SQLAlchemyError as err:
        return jsonify({'status': 'error', 'msg': err.msg})
        raise err


@api.route('/orders', defaults={'orderid': -1, 'customerid': -1, 'page': 1, 'perpage': 20}, methods=['GET'])
@api.route('/orders/<int:page>/<int:perpage>', defaults={'orderid': -1, 'customerid': -1}, methods=['GET'])
@api.route('/orders/<int:orderid>', defaults={'customerid': -1, 'page': 1, 'perpage': 20}, methods=['GET'])
@api.route('/orders/c/<int:customerid>', defaults={'orderid': -1, 'page': 1, 'perpage': 20}, methods=['GET'])
@jwt_required
def orders(orderid, customerid, page, perpage):
    sortParam = ""
    if request.args.get('sort'):
        sortParam = request.args.get('sort').replace("_", " ")
    if request.args.get('s'):
        searchVar = request.args.get('s')
        orders = Order.query.filter(
         func.lower(cast(Order.id, db.String)).contains(searchVar) |
         func.lower(cast(Order.orderdate, db.String)).contains(searchVar) |
         func.lower(cast(Order.customerid, db.String)).contains(searchVar)
        ).order_by(sortParam)
        return jsonify(orders=[o._asdict() for o in orders.all()])
    if customerid == -1 and orderid == -1:
        page, lastpage = correctPage(page, Order.query.count(), perpage)
        orders = Order.query.order_by(sortParam).paginate(per_page=perpage, page=page).items
        return jsonify(orders=[o._asdict() for o in orders], numpages=ceil(lastpage))
    elif orderid == -1:
        orders = Order.query.order_by(sortParam).filter_by(customerid=customerid).all()
        return jsonify(orders=[o._asdict() for o in orders])
    elif customerid == -1:
        order = Order.query.filter_by(id=orderid).one()
        return jsonify(order=order._asdict())



@api.route('/categories', methods=['GET'])
def categories():
    categories = Category.query.all()
    return jsonify(categories=[c._asdict() for c in categories])


@api.route('/users', defaults={'page': 1, 'perpage': 20}, methods=['GET'])
@api.route('/users/<int:page>/<int:perpage>', methods=['GET'])
@jwt_required
def get_users(page, perpage):
    sortParam = ""
    if request.args.get('sort'):
        sortParam = request.args.get('sort').replace("_", " ")
    if request.args.get('s'):
        searchVar = request.args.get('s')
        users = Customer.query.filter(
         func.lower(cast(Customer.id, db.String)).contains(searchVar) |
         func.lower(cast(Customer.username, db.String)).contains(searchVar) |
         func.lower(cast(Customer.email, db.String)).contains(searchVar) |
         func.lower(cast(Customer.firstname, db.String)).contains(searchVar) |
         func.lower(cast(Customer.lastname, db.String)).contains(searchVar)).order_by(sortParam)
        return jsonify(users=[u._asdict() for u in users.all()])
    else:
        page, lastpage = correctPage(page, Customer.query.count(), perpage)
        users = Customer.query.order_by(sortParam).paginate(per_page=perpage, page=page).items
        return jsonify(users=[u._asdict() for u in users], numpages=ceil(lastpage))


@api.route('/users', methods=['POST'])
def create_user():
    required_fields = {'username', 'email', 'password'}
    user_json = request.json

    if user_json is None:
        return jsonify({"msg": "Userdata malformed."}), HTTPStatus.BAD_REQUEST

    user_json = {k: v for k, v in user_json.items() if v}
    fields = set(user_json.keys())
    if fields < required_fields:
        missing = ', '.join(required_fields - fields)
        return jsonify({"msg": "Missing fields: %s." % missing}), HTTPStatus.BAD_REQUEST

    query_filter = or_(User.username == user_json['username'],
     User.email == user_json['email'])

    existing_user = Customer.query.filter(query_filter).one()

    if existing_user is not None:
        return jsonify({
         "msg": "Username or email already in use."
        }), HTTPStatus.BAD_REQUEST

    new_user = Customer(**user_json)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user._asdict())


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = Customer.query.filter_by(id=id).one()
    if user:
        user.beingedited = True
        db.session.commit()
        return jsonify(user=user._asdict())
    else:
        return jsonify({"msg": "User with %s not found." % id}), HTTPStatus.NOT_FOUND


@api.route('/users/<int:id>', methods=['PUT'])
@jwt_required
def update_user(id):
    updated_user = request.json
    if updated_user is None or id != updated_user.get('id'):
        return jsonify({"msg": "No or wrong user was provided."}), HTTPStatus.BAD_REQUEST
    user = Customer.query.with_for_update().filter_by(id=updated_user['id']).one()
    if user:
        if user.version_id == updated_user['version_id']:
            for key, value in updated_user.items():
                setattr(user, key, value)
            user.beingedited = False
            db.session.commit()
            return jsonify(user=user._asdict())
        else:
            db.session.rollback()
            return jsonify({
             "msg": "User has been modified by someone else."
            }), HTTPStatus.CONFLICT
    else:
        db.session.rollback()
        return jsonify({"msg": "User with %s not found." % id}), HTTPStatus.NOT_FOUND


@api.route('/users/<int:id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    user = Customer.query.filter_by(id=id).one()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User with id %s deleted." % id})
    else:
        return jsonify({"msg": "User with id %s not found." % id}), HTTPStatus.NOT_FOUND


@api.errorhandler(404)
@api.errorhandler(405)
def _handle_api_error(ex):
    if request.path.startswith('/api/'):
        return jsonify(ex.to_dict())
    else:
        return ex


def correctPage(page, anz, perpage):
    """Korrigiert die Seitenzahl, je nachdem wie viele Einträge auf einer Seite sind"""
    if page < 1:
        page = 1
    if page >= anz / perpage:  # setze seite auf das maximum, wenn man von kleiner perpage auf große wechselt (Auf letzer seite)
        page = int(anz / perpage)
    return page, anz / perpage
