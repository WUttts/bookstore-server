from flask import request, session, jsonify


# @app.before_first_request第一次请求 被执行
def before_first_request(app):
    @app.before_first_request
    def handle_before_first_request():
        print("第一次请求 被执行")


# @app.before_request每次请求都会执行的钩子
def before_request(app):
    @app.before_request
    def handle_before_request():
        if request.path != "/api/v1.0/sign_in":
            user_info = session.get("user_info")
            if user_info is None:
                return jsonify(code=403, message="You are not authorized to log in")


def after_request(app):
    @app.after_request
    def handle_after_request(response):
        print("每次请求没有异常 被执行")
        return response


def teardown_request(app):
    @app.teardown_request
    def handle_teardown_request(response):
        print("无论有无异常都 被执行")
        return response
