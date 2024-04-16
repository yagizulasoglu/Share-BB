"""Flask App for Flask Cafe."""

import os
from dotenv import load_dotenv

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

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

# toolbar = DebugToolbarExtension(app)

connect_db(app)
