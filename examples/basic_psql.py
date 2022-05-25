from psycopg2 import connect  # Changed from '/basic.py'
from pysql import Column, Integer, MetaData, PySQL, Text

db: PySQL = PySQL(
    engine='postgresql',  # Changed from '/basic.py'
    connection=connect(dsn=''),  # Changed from '/basic.py'
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
