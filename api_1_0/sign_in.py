from . import api
from flask import jsonify, request, current_app, session
from models import User, DBSession


@api.route("/sign_in", methods=["POST"])
def sign_in():
    req_dict = request.get_json()
    name = req_dict.get("name")
    password = req_dict.get("password")
    if not all([name, password]):
        return jsonify(code=400, message="incomplete parameters")
    try:
        dbsession = DBSession()
        result = dbsession.query(User.id, User.name, User.is_admin).filter(User.name == name, User.password == password).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(cdoe=500, message="server error")
    if result is None:
        return jsonify(code=401, message="wrong user name or password")
    user_data = dict(zip(result.keys(), result))
    dbsession.close()
    session["user_info"] = user_data
    return jsonify(code=200, message="ok!")

