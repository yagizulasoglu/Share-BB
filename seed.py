"""Initial data."""

from models import User, Listing, db, ImagePath


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


#######################################
# add listings

l1 = Listing(
    title="Beautiful House with a Massive Backyard",
    description='Best House in the Town',
    address="3966 24th St",
    user_id=u1_id
)

l2 = Listing(
    title='Apartment with a Huge Balcony',
    description='A cozy apartment with a balcony in the downtown.',
    address='440 Grand Ave',
    user_id=u1_id
)

db.session.add_all([l1, l2])
db.session.commit()

l1_id = l1.id
l2_id = l2.id

i1 = ImagePath(
    path = 'pear/filename',
    listing_id = l1_id
)

i2 = ImagePath(
    path = 'test.jpeg',
    listing_id = l2_id
)

db.session.add_all([i1, i2])
db.session.commit()


#######################################
# cafe maps

# c1.save_map()
# c2.save_map()
#
# db.session.commit()
