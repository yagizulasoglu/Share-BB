"""Data models for Share B&B"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMAGE_URL = (
    "https://icon-library.com/images/default-user-icon/" +
    "default-user-icon-28.jpg")


class User(db.Model):
    """User in the system"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    image_path = db.Column(
        db.String(255),
        # nullable=False,
        default="test.jpeg",
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Listing(db.Model):
    """Rental place in the system"""

    __tablename__ = "listings"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    title = db.Column(
        db.String(60),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default="",
    )

    address = db.Column(
        db.String(150),
        nullable=False,
    )

    daily_price = db.Column(
        db.Integer,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User', backref="listings")

    images = db.relationship('ImagePath', backref='listings',)

    @classmethod
    def register(cls, title, description, address, daily_price, user_id):
        """Registers Listing."""

        listing = Listing(
            title=title,
            description=description,
            address=address,
            daily_price=daily_price,
            user_id=user_id
        )

        db.session.add(listing)
        return listing


class ImagePath(db.Model):
    __tablename__ = "image_paths"

    path = db.Column(
        db.Text,
        primary_key=True,
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False,
    )

    @classmethod
    def create(cls, path, listing_id):
        """Creates a Path."""

        imagepath = ImagePath(
            path=path,
            listing_id=listing_id
        )

        db.session.add(imagepath)
        return imagepath


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
