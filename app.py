"""Flask App for Flask Cafe."""

import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from forms import AddListingForm, CSRFProtection, UserAddForm, LoginForm, UserUpdateForm, EditListingForm
from sqlalchemy.exc import IntegrityError

import boto3


from flask import Flask, render_template, flash, redirect, session, g, jsonify, request
# # from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import or_


from models import connect_db, User, db, Listing, ImagePath
load_dotenv()

CURR_USER_KEY = "curr_user"
BUCKET = os.environ.get('BUCKET')

BUCKET_BASE_URL = f'https://{BUCKET}.s3.us-east-2.amazonaws.com/'
print(BUCKET_BASE_URL)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///sharebb')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['AWS_SECRET_KEY'] = os.environ.get('AWS_SECRET_KEY')
app.config['ACCESS_KEY'] = os.environ.get('ACCESS_KEY')

app.config['WTF_CSRF_ENABLED'] = False

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = Truea

# toolbar = DebugToolbarExtension(app)

connect_db(app)

s3 = boto3.client(
    "s3",
    "us-east-1",
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
)


def add_image_to_bucket(content, img, listing_id):
    path = f'listing/{listing_id}/{img}'
    s3.put_object(Bucket=os.environ.get('BUCKET'),
                  Key=path, Body=content)
    return path


def add_pp_to_bucket(content, image, user_id):
    path = f'user/{user_id}/{image}'
    s3.put_object(Bucket=os.environ.get('BUCKET'),
                  Key=path, Body=content)
    return path



##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we are logged in add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_only_form():
    """Add a CSRF-only form so that every route can use it."""

    g.csrf_form = CSRFProtection()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    do_logout()

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.commit()

            image_file = request.files['image']
            image_content = image_file.read()
            path = add_pp_to_bucket(
                image_content, form.image.data.filename, user.id)

            user.image_path = path
            db.session.commit()


        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    form = LoginForm()

    if g.user:
        flash("You are already logged in", "danger")
        return redirect("/")

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data,
        )

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials", "danger")

    return render_template('users/login.html', form=form)


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""

    form = g.csrf_form

    if not form.validate_on_submit() or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
    print("We are here")
    do_logout()

    flash("You have successfully logged out.", "success")
    return redirect("/login")


@app.get('/')
def homepage():
    return render_template("base.html")

##############################################################################
# User routes:


@app.get('/users')
def list_users():
    """Page with listing of users"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    users = User.query.all()

    return render_template("users/users.html", users=users, url = BUCKET_BASE_URL)


@app.get('/users/<int:user_id>')
def show_user(user_id):
    """Show user profile"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    return render_template("users/profile.html", user=user, url= BUCKET_BASE_URL)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Edit user profile"""

    if not g.user or not g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserUpdateForm(obj=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.image_url = form.image_url.data

        try:
            db.session.commit()
            return redirect(f"/users/{user.id}")
        except IntegrityError:
            flash("Try Again", "danger")

    return render_template("users/edit.html", form=form, user_id=user.id, url = BUCKET_BASE_URL)


@app.post("/users/delete")
def delete_user():
    """Delete a user"""

    form = g.csrf_form

    if not form.validate_on_submit() or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout

    db.session.delete(g.user)
    db.session.commit()

    flash("User deleted.", "success")
    return redirect("/signup")


@app.get('/listings')
def list_listings():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    listings = Listing.query.all()

    return render_template("listings/listing.html", listings=listings, url = BUCKET_BASE_URL)


@app.route('/add-listing', methods=["GET", "POST"])
def add_listing():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = AddListingForm()

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if form.validate_on_submit():

        try:
            listing = Listing.register(
                title=form.title.data,
                description=form.description.data,
                address=form.address.data,
                daily_price=form.daily_price.data,
                user_id=g.user.id
            )
            db.session.commit()

            image_file = request.files['image']
            image_content = image_file.read()
            path = add_image_to_bucket(
                image_content, form.image.data.filename, listing.id)
            new_path = ImagePath.create(path, listing.id)
            db.session.add(new_path)
            db.session.commit()

        except IntegrityError:
            return render_template('listings/add-listing.html', form=form)

        return redirect("/")

    else:
        return render_template('listings/add-listing.html', form=form)


@app.get('/listings/<int:listing_id>')
def show_listing(listing_id):
    """Show a listing"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    listing = Listing.query.get_or_404(listing_id)

    return render_template("listings/info.html", listing=listing, url = BUCKET_BASE_URL)



@app.route('/listings/<int:listing_id>/edit', methods=["GET", "POST"])
def edit_listing(listing_id):
    """Edit user profile"""
    listing = Listing.query.get_or_404(listing_id)

    if not g.user or g.user.id != listing.user_id :
        flash("Access unauthorized.", "danger")
        return redirect("/")


    form = EditListingForm(obj=listing)
    if form.validate_on_submit():
        try:
            listing.title=form.title.data,
            listing.description=form.description.data,
            listing.address=form.address.data,
            listing.daily_price=form.daily_price.data,

            db.session.commit()

            image_file = request.files['image']
            image_content = image_file.read()
            path = add_image_to_bucket(
                image_content, form.image.data.filename, listing.id)
            new_path = ImagePath.create(path, listing.id)
            db.session.add(new_path)
            db.session.commit()
            flash("Listing Updated.", "success")
            return redirect(f'/listings/{listing.id}')

        except IntegrityError:
            return render_template('listings/edit-listing.html', form=form)


    return render_template("listings/edit-listing.html", form=form)


# @app.route('/add-listing', methods=['GET', 'POST'])
# def add_listing():

#     form = AddAListingForm()

#     if form.validate_on_submit():
#         filename = form.Image.data.filename
#         image_file = request.files['Image']
#         image_content = image_file.read()
#         add_image_to_bucket(image_content, filename, 'pear')

#     else:
#         return render_template('add-listing.html', form=form)

#     print(form.Image.data, "#############################")

#     return render_template('add-listing.html', form=form)


@app.get('/get-photo')
def get_photo():

    # s3 = boto3.client(
    #     "s3",
    #     "us-east-1",
    #     aws_access_key_id=os.environ.get('ACCESS_KEY'),
    #     aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    # )

    image_src = "https://sharebandb1234.s3.amazonaws.com/test123.jpeg"
    # breakpoint()
    # image_data = image['Body'].read()
    # image = Image.open(BytesIO(image_data))

    return render_template('get-photo.html', image_src=image_src,)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404
