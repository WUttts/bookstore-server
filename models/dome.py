from models import DBSession, User, Stock
import datetime

try:
    user1 = User(name="admin", password="p455w0rd", is_admin=True)
    user2 = User(name="user1", password="p455w0rd", is_admin=False)
    user3 = User(name="user2", password="p455w0rd", is_admin=False)
    dbsession = DBSession()
    dbsession.add_all([user1, user2, user3])
    dbsession.commit()
    dbsession.close()
except Exception as e:
    print(e)


try:
    dbsession = DBSession()
    for x in range(100):
        dbsession.add(Stock(id="编号{0}".format(x), book_name="测试", author="测试", release_time=datetime.datetime.now(), message="描述测试描述测试描述测试", price=100, retail_price=120, stock=18, picture_id=1))
        dbsession.commit()
    dbsession.close()
except Exception as e:
    print(e)



