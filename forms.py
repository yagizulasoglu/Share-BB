"""Forms for ShareB&B."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, IntegerField, DateField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, URL, Optional


class CSRFProtection(FlaskForm):
    """CSRFProtection form, intentionally has no fields."""


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    email = StringField(
        'E-mail',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )

    image = FileField('text', validators=[InputRequired()])


class UserUpdateForm(FlaskForm):
    '''Form for updating a user'''
    email = StringField(
        'E-mail',
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    image_url = FileField('text', validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )


class AddListingForm(FlaskForm):
    """Login form."""

    title = StringField(
        'Title',
        validators=[InputRequired(), Length(max=30)],
    )
    description = StringField(
        'Description',
        validators=[InputRequired(), Length(max=1000)],
    )

    address = StringField(
        'Address',
        validators=[InputRequired(), Length(max=75)],
    )

    daily_price = IntegerField(
        'Daily Price',
        validators=[InputRequired()],
    )

    image = FileField('text', validators=[InputRequired()])


class EditListingForm(FlaskForm):
    """Edit listing form."""

    title = StringField(
        'Title',
        validators=[InputRequired(), Length(max=30)],
    )
    description = StringField(
        'Description',
        validators=[InputRequired(), Length(max=1000)],
    )

    address = StringField(
        'Address',
        validators=[InputRequired(), Length(max=75)],
    )

    daily_price = IntegerField(
        'Daily Price',
        validators=[InputRequired()],
    )

    image = FileField('text')


class ReserveListingForm(FlaskForm):
    """Edit listing form."""

    start_date = DateField(
        'Start Date',
        validators=[InputRequired()],
    )

    end_date = DateField(
        'End Date',
        validators=[InputRequired()],
    )


class MessageForm(FlaskForm):
    '''Form for sending a message'''
    content = TextAreaField('text', validators=[InputRequired()])


class CSRFForm (FlaskForm):
    """Form for CSRF validation only"""
