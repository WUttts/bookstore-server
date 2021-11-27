from . import api
from flask import request, current_app, jsonify, session
from models import DBSession, Cart, Stock, Order, File
import datetime


@api.route("/add_order", methods=['post'])
def add_order():
    try:
        user_id = session.get("user_info").get("id")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=403, message="You are not authorized to log in")
    req_dict = request.get_json()
    book_id = req_dict.get("book_id")
    books_number = req_dict.get("books_number")
    if not all([book_id, books_number]):
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        stock = dbsession.query(Stock).filter(Stock.id == book_id).first()
        if stock.stock < books_number:
            return jsonify(code=401, message="insufficient inventory")
        unit_price = stock.price
        price = books_number * unit_price
        postage = books_number + 2
        res = Order(book_id=book_id, user_id=user_id, price=price, postage=postage, number=books_number)
        dbsession.add(res)
        dbsession.commit()
        order_id = res.id
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    return jsonify(code=200, data={"id": order_id})


@api.route("/get_order", methods=['get'])
def get_order():
    try:
        user_id = session.get("user_info").get("id")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=403, message="You are not authorized to log in")
    id = request.args.get("id")
    if id is None:
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        res = dbsession.query(Order.id, Order.price, Order.number, Order.postage, Stock.id.label("book_id"), File.url, Stock.book_name, Stock.author, Stock.message).filter(Order.book_id == Stock.id, Stock.picture_id == File.id, Order.user_id == user_id, Order.id == id).first()
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    data = dict(zip(res.keys(), res))
    return jsonify(code=200, data=data)



@api.route("/confirm_order", methods=['post'])
def confirm_order():
    try:
        user_id = session.get("user_info").get("id")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=403, message="You are not authorized to log in")
    req_dict = request.get_json()
    order_id = req_dict.get("order_id")
    if order_id is None:
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        res = dbsession.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
        res.update_time = datetime.datetime.now()
        res.is_payment = True
        res1 = dbsession.query(Stock).filter(Stock.id == res.book_id).first()
        res1.stock = res1.stock - res.number
        dbsession.query(Cart).filter(Cart.stock_id == res.book_id).delete()
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    return jsonify(code=200, message="ok!")

