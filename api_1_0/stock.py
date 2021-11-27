from . import api
from flask import jsonify, request, current_app, session
from models import DBSession, Stock, File
import datetime
from sqlalchemy import func


@api.route("/add_books", methods=["post"])
def add_books():
    identity = session.get("user_info")
    is_admin = identity.get("is_admin")
    if not is_admin:
        return jsonify(code=401, message="no permission")
    req_dict = request.get_json()
    id = req_dict.get("id")
    book_name = req_dict.get("book_name")
    author = req_dict.get("author")
    release_time = req_dict.get("release_time")
    message = req_dict.get("message")
    price = req_dict.get("price")
    retail_price = req_dict.get("retail_price")
    stock = req_dict.get("stock")
    picture_id = req_dict.get("picture_id")
    if not all([id, book_name, author, release_time, message, price, retail_price, stock, picture_id]):
        return jsonify(code=400, message="incomplete parameters")
    if price > 200:
        return jsonify(code=400, message="the unit price cannot exceed £ 200")
    if retail_price > 200:
        return jsonify(code=400, message="the retail price cannot exceed ￡ 200")
    if stock > 20:
        return jsonify(code=400, message="inventory cannot exceed 20")
    release_time = datetime.datetime.strptime(release_time, '%Y-%m-%d %H:%M:%S')
    try:
        dbsession = DBSession()
        res = dbsession.query(Stock).filter(Stock.id == id).first()
        if res is None:
            result = Stock(id=id, book_name=book_name, author=author, release_time=release_time, message=message,price=price, retail_price=retail_price, stock=stock, picture_id=picture_id)
            dbsession.add(result)
        else:
            res.book_name = book_name
            res.author = author
            res.release_time = release_time
            res.message = message
            res.price = price
            res.retail_price = retail_price
            res.stock = stock
            res.picture_id = picture_id
            res.update_time = datetime.datetime.now()
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    return jsonify(code=200, message="ok!")


@api.route("del_books", methods=["post"])
def del_books():
    identity = session.get("user_info")
    is_admin = identity.get("is_admin")
    if not is_admin:
        return jsonify(code=401, message="no permission")
    req_dict = request.get_json()
    id = req_dict.get("id")
    if id is None:
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        dbsession.query(Stock).filter(Stock.id == id).delete()
        dbsession.commit()
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    return jsonify(code=200, message="ok!")


@api.route("modify_books", methods=["post"])
def modify_books():
    identity = session.get("user_info")
    is_admin = identity.get("is_admin")
    if not is_admin:
        return jsonify(code=401, message="no permission")
    req_dict = request.get_json()
    id = req_dict.get("id")
    book_name = req_dict.get("book_name")
    author = req_dict.get("author")
    release_time = req_dict.get("release_time")
    message = req_dict.get("message")
    price = req_dict.get("price")
    retail_price = req_dict.get("retail_price")
    stock = req_dict.get("stock")
    picture_id = req_dict.get("picture_id")
    if not all([id, book_name, author, release_time, message, price, retail_price, stock, picture_id]):
        return jsonify(code=400, message="incomplete parameters")
    if price > 200:
        return jsonify(code=400, message="the unit price cannot exceed £ 200")
    if retail_price > 200:
        return jsonify(code=400, message="the retail price cannot exceed ￡ 200")
    if stock > 20:
        return jsonify(code=400, message="inventory cannot exceed 20")
    release_time = datetime.datetime.strptime(release_time, '%Y-%m-%d %H:%M:%S')
    try:
        dbsession = DBSession()
        res = dbsession.query(Stock).filter(Stock.id == id).first()
        if res is None:
            return jsonify(code=400, message="the book no longer exists")
        else:
            res.book_name = book_name
            res.author = author
            res.release_time = release_time
            res.message = message
            res.price = price
            res.retail_price = retail_price
            res.stock = stock
            res.picture_id = picture_id
            dbsession.commit()
            dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    return jsonify(code=200, message="ok!")


@api.route("get_books_item", methods=["get"])
def get_books_item():
    identity = session.get("user_info")
    is_admin = identity.get("is_admin")
    if not is_admin:
        return jsonify(code=401, message="no permission")
    id = request.args.get("id")
    if id is None:
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        result = dbsession.query(Stock.id, Stock.book_name, Stock.author, Stock.release_time, Stock.message, Stock.price, Stock.retail_price, Stock.stock, File.id.label("file_id"), File.url).filter(Stock.id == id, Stock.picture_id == File.id).first()
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    if result is None:
        return jsonify(code=400, message="the book no longer exists")
    else:
        data = dict(zip(result.keys(), result))
        return jsonify(code=200, data=data)


@api.route("get_books_list", methods=["get"])
def get_books_list():
    identity = session.get("user_info")
    is_admin = identity.get("is_admin")
    if not is_admin:
        return jsonify(code=401, message="no permission")
    try:
        page_size, page_number = int(request.args.get("page_size")), int(request.args.get("page_number"))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        count = dbsession.query(func.count(Stock.id)).scalar()
        results = dbsession.query(Stock.id, Stock.book_name, Stock.author, Stock.release_time, Stock.message, Stock.price, Stock.retail_price, Stock.stock, File.id.label("file_id"), File.url).order_by(Stock.update_time.desc()).filter(Stock.picture_id == File.id).offset((page_number - 1) * page_size).limit(page_size)
        dbsession.close()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="mysql error")
    data_list = [dict(zip(result.keys(), result)) for result in results]
    data = {
        "count": count,
        "data": data_list
    }
    return jsonify(code=200, data=data)
