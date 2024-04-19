"""Initial data."""

from models import User, Listing, db, ImagePath, Reservation
from datetime import date


db.drop_all()
db.create_all()


#######################################
# add users

ua = User.signup(
    username="admin",
    email="admin@test.com",
    password="secret",
)

u1 = User.signup(
    username="test",
    email="test@test.com",
    password="secret",
)

db.session.add_all([ua, u1])
db.session.commit()

u1_id = u1.id
ua_id = ua.id


#######################################
# add listings

l1 = Listing(
    title="Beautiful House with a Massive Backyard",
    description='Best House in the Town',
    address="3966 24th St",
    daily_price = 1000,
    user_id=ua_id
)

l2 = Listing(
    title='Apartment with a Huge Balcony',
    description='A cozy apartment with a balcony in the downtown.',
    address='440 Grand Ave',
    daily_price = 50,
    user_id=ua_id
)

l3 = Listing(
    title='Haunted House with a Cozy Atmosphere',
    description='Enjoy your time here while the ghost is sleeping. He is harmless',
    address='123 Casper St',
    daily_price = 1,
    user_id=u1_id
)

db.session.add_all([l1, l2, l3])
db.session.commit()

l1_id = l1.id
l2_id = l2.id
l3_id = l3.id

i1 = ImagePath(
    path='house1.jpg',
    listing_id=l1_id
)

i2 = ImagePath(
    path='house2.jpg',
    listing_id=l1_id
)

i3 = ImagePath(
    path='apartment1.jpg',
    listing_id=l2_id
)

i4 = ImagePath(
    path='apartment2.jpg',
    listing_id=l2_id
)

i5 = ImagePath(
    path='casper1.jpg',
    listing_id=l3_id
)

i6 = ImagePath(
    path='casper2.jpg',
    listing_id=l3_id
)


db.session.add_all([i1, i2, i3, i4, i5, i6])
db.session.commit()


r1 = Reservation(
    user_id=u1_id,
    listing_id=l1_id,
    start_date=date(2032,11,5),
    end_date=date(2032,11,12),
    total_cost=100
)

db.session.add_all([r1])
db.session.commit()

