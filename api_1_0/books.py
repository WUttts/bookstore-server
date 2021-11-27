from . import api
from flask import request, current_app, jsonify
from models import DBSession, Stock, File
from sqlalchemy import func
import datetime


@api.route("/get_book_list", methods=['get'])
def get_book_list():
    try:
        page_size, page_number = int(request.args.get("page_size")), int(request.args.get("page_number"))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        count = dbsession.query(func.count(Stock.id)).filter(Stock.release_time <= datetime.datetime.now()).scalar()
        results = dbsession.query(Stock.id, Stock.book_name, Stock.author, Stock.release_time, Stock.message, Stock.price, Stock.retail_price, Stock.stock, File.id.label("file_id"), File.url).order_by(Stock.update_time.desc()).filter(Stock.picture_id == File.id, Stock.release_time <= datetime.datetime.now()).offset((page_number - 1) * page_size).limit(page_size)
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
