s3 = boto3.client(
    "s3",
    "us-east-1",
    aws_access_key_id=os.environ.get('ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
)


with open('test.jpeg', 'rb') as data:
    s3.put_object(Bucket = os.environ.get('BUCKET'), Key='test.jpeg', Body=data)


image = s3.get_object(Bucket = os.environ.get('BUCKET'), Key= 'test.jpeg')
image_data = image['Body'].read()
image = Image.open(BytesIO(image_data))
image.show()

breakpoint()

