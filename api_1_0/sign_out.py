from . import api
from flask import session, jsonify


@api.route("/sign_out", methods=['get'])
def sign_out():
    try:
        session.clear()
    except Exception as e:
        return jsonify(code=500, message="server error")
    return jsonify(code=200, message="ok!")

