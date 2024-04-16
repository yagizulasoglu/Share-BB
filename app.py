"""Flask App for Flask Cafe."""

import os
from dotenv import load_dotenv

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

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

# toolbar = DebugToolbarExtension(app)

connect_db(app)

s3 = boto3.client(
    "s3",
    "us-east-1",
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
)


print((s3.list_buckets()).Buckets, "#####################################")
# for bucket in s3.buckets.all():
#     print(bucket.name)

with open('test.jpeg', 'rb') as data:
    s3.put_object(s3.list_buckets().Buckets[0].Name).put_object(
        Key='test.jpeg', Body=data)

# try:
#     response = s3_client.put_object(
#         Bucket=s3.Buckets.list_buckets[0].Name,
#         Key=object_key
#     )
# except:
#     print("error")


# response = s3_client.put_object(
#     Bucket='your-bucket-name',  # Name of the S3 bucket
#     Key='path/to/your/object/file.txt',  # Key (path) where the object will be stored within the bucket
#     Body=b'Object content',  # Data (content) of the object to be uploaded
#     # ContentType='text/plain',  # Optional: Content type of the object (MIME type)
#     # ACL='private',  # Optional: Access Control List for the object (e.g., 'private', 'public-read')
#     # Metadata={'key': 'value'},  # Optional: Metadata associated with the object
#     # StorageClass='STANDARD',  # Optional: Storage class of the object (e.g., 'STANDARD', 'STANDARD_IA')
#     # ServerSideEncryption='AES256'  # Optional: Server-side encryption algorithm (e.g., 'AES256')
# )
