"""Flask App for Flask Cafe."""

import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from forms import AddAListingForm

import boto3


from flask import Flask, render_template, flash, redirect, session, g, jsonify, request
# # from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import or_


from models import connect_db

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///sharebb')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['AWS_SECRET_KEY'] = os.environ.get('AWS_SECRET_KEY')
app.config['ACCESS_KEY'] = os.environ.get('ACCESS_KEY')

app.config['WTF_CSRF_ENABLED'] = False

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = Truea

# toolbar = DebugToolbarExtension(app)

s3 = boto3.client(
    "s3",
    "us-east-1",
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
)


def add_image_to_bucket(content, filename):
    print(filename, "**************")
    s3.put_object(Bucket=os.environ.get('BUCKET'),
                  Key=filename, Body=content)


@app.route('/add-listing', methods=['GET', 'POST'])
def add_listing():

    form = AddAListingForm()

    if form.validate_on_submit():
        filename = form.Image.data.filename
        image_file = request.files['Image']
        image_content = image_file.read()
        add_image_to_bucket(image_content, filename)

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

    return render_template('get-photo.html', image_src=image_src)
