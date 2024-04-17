"""Flask App for Flask Cafe."""

import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from forms import AddAListingForm, CSRFProtection, UserAddForm, LoginForm
from sqlalchemy.exc import IntegrityError

import boto3


from flask import Flask, render_template, flash, redirect, session, g, jsonify, request
# # from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import or_


from models import connect_db, User, db, Listing
load_dotenv()

CURR_USER_KEY = "curr_user"

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
                image_url=form.image_url.data or User.image_url.default.arg,
            )
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

    return render_template("users/users.html", users=users)




@app.get('/listings')
def list_listings():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    listings = Listing.query.all()


    return render_template("listings/listing.html", listings=listings, image_path = 'test.jpeg')






def add_image_to_bucket(content, filename, listing):
    print(filename, "**************")
    s3.put_object(Bucket=os.environ.get('BUCKET'),
                  Key=f'{listing}/{filename}', Body=content)


@app.route('/add-listing', methods=['GET', 'POST'])
def add_listing():

    form = AddAListingForm()

    if form.validate_on_submit():
        filename = form.Image.data.filename
        image_file = request.files['Image']
        image_content = image_file.read()
        add_image_to_bucket(image_content, filename, 'pear')

    else:
        return render_template('add-listing.html', form=form)

    print(form.Image.data, "#############################")

    return render_template('add-listing.html', form=form)


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


