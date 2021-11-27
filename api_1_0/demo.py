from . import api


@api.route("/")
def hello_world():
    return "Hello,World!"


@api.route('/index', methods=["post"])
def index():
    return 'index page'
