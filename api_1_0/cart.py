from . import api
from flask import request, current_app, jsonify, session
from models import DBSession, Cart, Stock, File
from sqlalchemy import func
import datetime


@api.route("/add_cart", methods=['post'])
def add_cart():
    req_dict = request.get_json()
    book_id = req_dict.get("book_id")
    books_number = req_dict.get("books_number")
    if not all([book_id, books_number]):
        return jsonify(code=400, message="incomplete parameters")
    try:
        user_id = session.get("user_info").get("id")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=403, message="You are not authorized to log in")
    dbsession = DBSession()
    try:
        res = dbsession.query(Cart).filter(Cart.stock_id == book_id, Cart.user_id == user_id).first()
        if res is None:
            car = Cart(user_id=user_id, stock_id=book_id, books_number=books_number)
            dbsession.add(car)
        else:
            res.books_number = res.books_number + books_number
            res.update_time = datetime.datetime.now()
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    return jsonify(code=200, message="ok!")


@api.route("/del_cart", methods=['post'])
def del_cart():
    req_dict = request.get_json()
    id = req_dict.get("id")
    if id is None:
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        dbsession.query(Cart).filter(Cart.id == id).delete()
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    return jsonify(code=200, message="ok!")


@api.route("/modify_cart", methods=['post'])
def modify_cart():
    req_dict = request.get_json()
    id = req_dict.get("id")
    books_number = req_dict.get("books_number")
    if not all([id, books_number]):
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        res = dbsession.query(Cart).filter(Cart.id == id).first()
        res.books_number = books_number
        res.update_time = datetime.datetime.now()
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    return jsonify(code=200, message="ok!")


@api.route("/get_cart", methods=['get'])
def get_cart():
    try:
        user_id = session.get("user_info").get("id")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=403, message="You are not authorized to log in")
    try:
        page_size, page_number = int(request.args.get("page_size")), int(request.args.get("page_number"))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        count = dbsession.query(func.count(Cart.id)).filter(Cart.user_id == user_id).scalar()
        results = dbsession.query(Cart.id, Cart.books_number, Stock.id.label("book_id"), Stock.book_name, Stock.author, Stock.message, Stock.stock, File.url, Stock.price).order_by(Cart.update_time.desc()).filter(Cart.user_id == user_id, Cart.stock_id == Stock.id, Stock.picture_id == File.id).offset((page_number - 1) * page_size).limit(page_size)
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    data_list = [dict(zip(result.keys(), result)) for result in results]
    data = {
        "count": count,
        "data": data_list
    }
    return jsonify(code=200, data=data)


