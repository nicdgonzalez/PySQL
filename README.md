# PySQL - Object Relational Mapper

> Work in Progress

Implementing an object-relational mapper (ORM) from scratch using the
programming language, [Python](https://www.python.org/).

ORMs take a database and convert its attributes to objects to be used within
the programming language.


## Basic Examples
> There are more examples in the [/examples](./examples/) directory.

* Constructing a new Model:

```python
# file:: ./examples/basic.py
from sqlite3 import connect

from pysql import Column, Integer, MetaData, PySQL, Text

db: PySQL = PySQL(
    engine='sqlite3',
    connection=connect('db.sqlite3'),
    meta=MetaData()
)


class Prefixes(db.Model, name='prefixes'):
    guild_id = Column(Integer, primary_key=True)
    prefix = Column(Text, not_null=True, default='$')


# Inserting a value into the database:
db.session.insert(Prefixes(guild_id=0, prefix='!'))

# Query the database by using the model as a filter
# and providing a list of the values you want to return:
guild_prefix = db.query.fetchone(Prefixes(guild_id=0), select=['prefix'])
print(guild_prefix)  # Returns: ('!',)

# Updating a value in the database:
db.session.update(Prefixes(prefix='?'), filter={'guild_id': 0})

guild_prefix = db.query.fetchone(Prefixes(guild_id=0), select=['prefix'])
print(guild_prefix)  # Returns: ('?',)

# Delete the entry in the database where 'guild_id = 0':
db.session.delete(Prefixes(guild_id=0))

guild_prefix = db.query.fetchone(Prefixes(guild_id=0), select=['prefix'])
print(guild_prefix)  # Returns: None
```

* Referencing columns from another model:

```python
# file:: ./examples/foreign_key.py
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
```


## Version Naming

This library uses semantic versioning:

    MAJOR.MINOR.PATCH

Where an increment in:
- `MAJOR` = Incompatible changes (may require code to be updated).
- `MINOR` = Backwards compatible feature changes.
- `PATCH` = Backwards compatible bug fixes.