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

def add_image_to_bucket():
    s3 = boto3.client(
    "s3",
    "us-east-1",
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
)
    with open('test.jpeg', 'rb') as data:
        s3.put_object(Bucket = os.environ.get('BUCKET'), Key='test.jpeg', Body=data)





@app.route('/add-listing', methods=['GET', 'POST'])
def add_listing():

    form = AddAListingForm()

    add_image_to_bucket();

    return render_template('add-listing.html', form = form )