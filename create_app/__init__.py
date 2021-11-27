from flask import Flask
from sqlalchemy.sql.schema import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from config import config_map 

# python的标准模块，提供了各种各样的日志工具
import logging
from logging.handlers import RotatingFileHandler
from . import hook

# 设置日志级别（如果flask运行再DEBUG模式下，会忽略调日志级别控制器，会记录所有日志）
logging.basicConfig(level=logging.INFO)  # 只会记录到info级别，info级别后的就不会再执行
# 创建日志记录器，指明日志保存的路径，每个日志文件的大小，保存日志个数的上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级        输入日志的文件名：行数     日志信息
formatter = logging.Formatter("%(levelname)s %(filename)s:%(lineno)d %(message)s")
# 为刚刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    """
        创建flask的应用对象
        :param config_name: str 配置模式的模式名字 （"develop", "product"）
        :return: flask对象
    """
    app = Flask(__name__, static_folder="../static")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp.db'
    db = SQLAlchemy(app)
    app.config.from_object(config_map.get(config_name))
    hook.before_request(app)
    from api_1_0 import api
    app.register_blueprint(api, url_prefix="/api/v1.0")
    return app