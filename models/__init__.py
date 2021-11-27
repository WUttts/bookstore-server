from flask import Flask
from sqlalchemy.sql.schema import ForeignKey
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp.db'
db = SQLAlchemy(app)
import datetime


# 创建时间与更新时间
class Time(object):
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now)


class User(db.Model, Time):
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Stock(db.Model, Time):
    __tablename__ = "stock"
    id = db.Column(db.String(100), primary_key=True)
    book_name = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    release_time = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    retail_price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    picture_id = db.Column(db.Integer, ForeignKey("file.id"))


class File(db.Model):
    __tablename__ = "file"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(100), nullable=False)
    real_name = db.Column(db.String(100), nullable=False)
    file_type = db.Column(db.String(30), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(100), nullable=False)


class Cart(db.Model, Time):
    __tablename__ = "Cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_id = db.Column(db.String(100), ForeignKey("stock.id"))
    user_id = db.Column(db.Integer, ForeignKey("user_info.id"))
    books_number = db.Column(db.Integer, nullable=False)


class Order(db.Model, Time):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.String(100), ForeignKey("stock.id"))
    user_id = db.Column(db.Integer, ForeignKey("user_info.id"))
    number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    postage = db.Column(db.Float, nullable=False)
    is_payment = db.Column(db.Boolean, default=False)
    is_deliver_goods = db.Column(db.Boolean, default=False)
    receiving = db.Column(db.Boolean, default=False)


# 初始化数据模型：初始化数据模型时只会在数据库中创建继承db.Model类的数据模型
def init_db():
    db.create_all()


# 删除数据模型：删除数据模型时只会在数据库中删除继承db.Model类的数据模型
def drop_db():
   db.drop_all()

DBSession = db.session


# 请慎重运行本文件，本文件会初始化数据库
if __name__ == '__main__':
    drop_db()
    init_db()
    user1 = User(name="admin", password="p455w0rd", is_admin=True)
    user2 = User(name="user1", password="p455w0rd", is_admin=False)
    user3 = User(name="user2", password="p455w0rd", is_admin=False)
    dbsession = DBSession()
    dbsession.add_all([user1, user2, user3])
    dbsession.commit()
    dbsession.close()
