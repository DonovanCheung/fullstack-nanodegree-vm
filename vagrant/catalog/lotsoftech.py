#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Electronics, Device

engine = create_engine('sqlite:///electronics.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Laptop Devices
electronic1 = Electronics(name="laptops", id=1, user_id=1)
session.add(electronic1)
session.commit()

device1 = Device(user_id=1, name="MacBook Pro", id=1,
                 description="MacBook Pro made by Apple",
                 price="$1299.99", year="2020", brand="Apple",
                 electronics=electronic1)
session.add(device1)
session.commit()

device2 = Device(user_id=1, name="MacBook Air", id=2,
                 description="MacBook Air made by Apple",
                 price="$1099.99", year="2020", brand="Apple",
                 electronics=electronic1)
session.add(device2)
session.commit()

device3 = Device(user_id=1, name="XPS 13", id=3,
                 description="XPS 13 made by Dell",
                 price="$999.99", year="2020", brand="Dell",
                 electronics=electronic1)
session.add(device3)
session.commit()

device4 = Device(user_id=1, name="XPS 15", id=4,
                 description="XPS 15 made by Dell",
                 price="$1199.99", year="2020", brand="Dell",
                 electronics=electronic1)
session.add(device4)
session.commit()

device5 = Device(user_id=1, name="ZBook 15", id=5,
                 description="ZBook 15 made by HP",
                 price="$1299.99", year="2020", brand="HP",
                 electronics=electronic1)
session.add(device5)
session.commit()

device6 = Device(user_id=1, name="Pavilion x360", id=6,
                 description="Pavilion x360 made by HP",
                 price="$599.99", year="2020", brand="HP",
                 electronics=electronic1)
session.add(device6)
session.commit()

device7 = Device(user_id=1, name="Yoga 730", id=7,
                 description="Yoga 730 made by Lenovo",
                 price="$829.99", year="2020", brand="Lenovo",
                 electronics=electronic1)
session.add(device7)
session.commit()

device8 = Device(user_id=1, name="Nitro 5", id=8,
                 description="Nitro 5 made by Acer",
                 price="$749.99", year="2020", brand="Acer",
                 electronics=electronic1)
session.add(device8)
session.commit()

device9 = Device(user_id=1, name="Notebook 7", id=9,
                 description="Notebook 7 made by Samsung",
                 price="$799.99", year="2020", brand="Samsung",
                 electronics=electronic1)
session.add(device9)
session.commit()

device10 = Device(user_id=1, name="Surface Book 2", id=10,
                  description="Surface Book 2 made by Microsoft",
                  price="$1999.99", year="2020", brand="Microsoft",
                  electronics=electronic1)
session.add(device10)
session.commit()

# Tablet Devices
electronic2 = Electronics(name="tablets", id=2, user_id=1)
session.add(electronic2)
session.commit()

device1 = Device(user_id=1, name="iPad Pro", id=11,
                 description="iPad Pro made by Apple",
                 price="$799.99", year="2020", brand="Apple",
                 electronics=electronic2)
session.add(device1)
session.commit()

device2 = Device(user_id=1, name="iPad Air", id=12,
                 description="iPad Air made by Apple",
                 price="$499.99", year="2020", brand="Apple",
                 electronics=electronic2)
session.add(device2)
session.commit()

device3 = Device(user_id=1, name="iPad", id=13,
                 description="iPad made by Apple",
                 price="$329.99", year="2020", brand="Apple",
                 electronics=electronic2)
session.add(device3)
session.commit()

device4 = Device(user_id=1, name="iPad mini", id=14,
                 description="iPad mini made by Apple",
                 price="$399.99", year="2020", brand="Apple",
                 electronics=electronic2)
session.add(device4)
session.commit()

device5 = Device(user_id=1, name="Surface Pro 7", id=15,
                 description="Surface Pro 7 made by Microsoft",
                 price="$699.99", year="2020", brand="Microsoft",
                 electronics=electronic2)
session.add(device5)
session.commit()

device6 = Device(user_id=1, name="Surface Go", id=16,
                 description="Surface Go made by Microsoft",
                 price="$549.99", year="2020", brand="Microsoft",
                 electronics=electronic2)
session.add(device6)
session.commit()

device7 = Device(user_id=1, name="Surface Pro X", id=17,
                 description="Surface Pro X made by Microsoft",
                 price="$1599.99", year="2020", brand="Microsoft",
                 electronics=electronic2)
session.add(device7)
session.commit()

device8 = Device(user_id=1, name="Galaxy Tab A", id=18,
                 description="Galaxy Tab A made by Samsung",
                 price="$289.99", year="2020", brand="Samsung",
                 electronics=electronic2)
session.add(device8)
session.commit()

device9 = Device(user_id=1, name="Galaxy Tab S6", id=19,
                 description="Galaxy Tab S6 made by Samsung",
                 price="$549.99", year="2020", brand="Samsung",
                 electronics=electronic2)
session.add(device9)
session.commit()

device10 = Device(user_id=1, name="Kindle", id=20,
                  description="Kindle made by Amazon",
                  price="$129.99", year="2020", brand="Amazon",
                  electronics=electronic2)
session.add(device10)
session.commit()

# Phone Devices
electronic3 = Electronics(name="phones", id=3, user_id=1)
session.add(electronic3)
session.commit()

device1 = Device(user_id=1, name="iPhone 11", id=21,
                 description="iPhone 11 made by Apple",
                 price="$699.99", year="2020", brand="Apple",
                 electronics=electronic3)
session.add(device1)
session.commit()

device2 = Device(user_id=1, name="iPhone 11 Pro", id=22,
                 description="iPhone 11 Pro made by Apple",
                 price="$999.99", year="2020", brand="Apple",
                 electronics=electronic3)
session.add(device2)
session.commit()

device3 = Device(user_id=1, name="iPhone 11 Pro Max", id=23,
                 description="iPhone 11 Pro Max made by Apple",
                 price="$1099.99", year="2020", brand="Apple",
                 electronics=electronic3)
session.add(device3)
session.commit()

device4 = Device(user_id=1, name="Pixel 4", id=24,
                 description="Pixel 4 made by Google",
                 price="$699.99", year="2020", brand="Google",
                 electronics=electronic3)
session.add(device4)
session.commit()

device5 = Device(user_id=1, name="Pixel 4 XL", id=25,
                 description="Pixel 4 XL made by Google",
                 price="$749.99", year="2020", brand="Google",
                 electronics=electronic3)
session.add(device5)
session.commit()

device6 = Device(user_id=1, name="Galaxy Note10", id=26,
                 description="Galaxy Note10 made by Samsung",
                 price="$699.99", year="2020", brand="Samsung",
                 electronics=electronic3)
session.add(device6)
session.commit()

device7 = Device(user_id=1, name="Galaxy S10", id=27,
                 description="Galaxy S10 made by Samsung",
                 price="$599.99", year="2020", brand="Samsung",
                 electronics=electronic3)
session.add(device7)
session.commit()

# Video Game Console Devices
electronic4 = Electronics(name="video-game-consoles", id=4, user_id=1)
session.add(electronic4)
session.commit()

device1 = Device(user_id=1, name="Xbox One S", id=28,
                 description="Xbox One S made by Microsoft",
                 price="$199.99", year="2020", brand="Microsoft",
                 electronics=electronic4)
session.add(device1)
session.commit()

device2 = Device(user_id=1, name="Xbox One X", id=29,
                 description="Xbox One X made by Microsoft",
                 price="$299.99", year="2020", brand="Microsoft",
                 electronics=electronic4)
session.add(device2)
session.commit()

device3 = Device(user_id=1, name="PS4", id=30,
                 description="PS4 made by Sony",
                 price="$299.99", year="2020", brand="Sony",
                 electronics=electronic4)
session.add(device3)
session.commit()

device4 = Device(user_id=1, name="PS4 Pro", id=31,
                 description="PS4 Pro made by Sony",
                 price="$399.99", year="2020", brand="Sony",
                 electronics=electronic4)
session.add(device4)
session.commit()

device5 = Device(user_id=1, name="Switch", id=32,
                 description="Switch made by Nintendo",
                 price="$299.99", year="2020", brand="Nintendo",
                 electronics=electronic4)
session.add(device5)
session.commit()

print("Added electronic devices!")
