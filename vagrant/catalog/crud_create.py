from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MenuItem, Restaurant

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
myFirstRestaurant = Restaurant(name="Pizza Palace")
session.add(myFirstRestaurant) #In the staging zone
session.commit()


cheesepizza = MenuItem(name="Cheese Pizza",
                       description="Made with all Natrual"
                                   "ingredients",
                       course = "Entree",
                       price="$8.99",
                       restaurant=myFirstRestaurant # Foreign key
                       )
session.add(cheesepizza)
session.commit()
#Check if the record has been added:
print(session.query(Restaurant).all())
print(session.query(MenuItem).all())