from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MenuItem, Restaurant
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
    spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
except NoResultFound as e:
    print(e)
    quit(0)
print(spinach.restaurant.name)
session.delete(spinach)
session.commit()

try:
    spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
except NoResultFound as e:
    print(e)
