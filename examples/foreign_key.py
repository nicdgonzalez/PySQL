from sqlite3 import connect

from pysql import Column, Integer, MetaData, Numeric, PySQL, Text

db: PySQL = PySQL(
    engine='sqlite3',
    connection=connect('db.sqlite3'),
    meta=MetaData()
)


class Products(db.Model, name='products'):
    product_id = Column(Integer, primary_key=True)
    item_name = Column(Text)
    price = Column(Numeric, check='price > 0')


class Orders(db.Model, name='orders'):
    order_id = Column(Integer, primary_key=True)
    shipping_address = Column(Text)
    ...


class OrderItems(db.Model, name='order_items'):
    product_id = Column(
        Integer,
        primary_key=True,
        reference=Products.product_id
    )
    order_id = Column(
        Integer,
        primary_key=True,
        reference=Orders.order_id
    )
    quantity = Column(
        Integer,
        check='quantity >= 0'
    )
