from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MenuItem, Restaurant

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name="Veggie Burger")
for v in veggieBurgers:
    print(str(v.id) + "," + v.name + "," + str(v.price) + "," + str(v.restaurant.name))

for v in veggieBurgers:
    if v.price != "$2.99":
        v.price="$2.99"
        session.add(v)
session.commit()

veggieBurgers = session.query(MenuItem).filter_by(name="Veggie Burger")
for v in veggieBurgers:
    print(str(v.id) + "," + v.name + "," + str(v.price) + "," + str(v.restaurant.name))

