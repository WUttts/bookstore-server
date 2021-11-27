from . import api
from flask import session, jsonify


@api.route("/get_user_info")
def get_user_info():
    data = session.get("user_info")
    return jsonify(code=200, data=data)