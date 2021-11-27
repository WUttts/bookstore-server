# 从sqlalchemy.ext.declarative中导入declarative_base创建sqlalchemy的基类
from sqlalchemy.ext.declarative import declarative_base
# 从sqlalchemy中导入各种各样的数据类型，用于创建字段或者指定字段的数据类型
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
# create_engine创建数据库连接所需
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

# create_engine()用来初始化数据库连接引擎。SQLAlchemy用一个字符串表示连接信息：
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
engine = create_engine("mysql+mysqlconnector://root:wtp164614@localhost:3306/bookstore?charset=utf8mb4", max_overflow=5)
# 创建对象的基类:
Base = declarative_base()


# 创建时间与更新时间
class Time(object):
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now)


class User(Base, Time):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)


class Stock(Base, Time):
    __tablename__ = "stock"
    id = Column(String(100), primary_key=True)
    book_name = Column(String(30), nullable=False)
    author = Column(String(30), nullable=False)
    release_time = Column(DateTime, nullable=False)
    message = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    retail_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    picture_id = Column(Integer, ForeignKey("file.id"))


class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(100), nullable=False)
    real_name = Column(String(100), nullable=False)
    file_type = Column(String(30), nullable=False)
    file_size = Column(Integer, nullable=False)
    url = Column(String(100), nullable=False)


class Cart(Base, Time):
    __tablename__ = "Cart"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(String(100), ForeignKey("stock.id"))
    user_id = Column(Integer, ForeignKey("user_info.id"))
    books_number = Column(Integer, nullable=False)


class Order(Base, Time):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(String(100), ForeignKey("stock.id"))
    user_id = Column(Integer, ForeignKey("user_info.id"))
    number = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    postage = Column(Float, nullable=False)
    is_payment = Column(Boolean, default=False)
    is_deliver_goods = Column(Boolean, default=False)
    receiving = Column(Boolean, default=False)


# 初始化数据模型：初始化数据模型时只会在数据库中创建继承Base类的数据模型
def init_db():
    Base.metadata.create_all(engine)


# 删除数据模型：删除数据模型时只会在数据库中删除继承Base类的数据模型
def drop_db():
    Base.metadata.drop_all(engine)


# 创建一个配置过的Session类：Session可以视为会话，作为为打开与数据库的通话，这个类可以管理数据库的连接
DBSession = sessionmaker(bind=engine)


# 请慎重运行本文件，本文件会初始化数据库
if __name__ == '__main__':
    drop_db()
    init_db()
