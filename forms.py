"""Forms for ShareB&B."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, IntegerField, DateField, TextAreaField, MultipleFileField
from wtforms.validators import InputRequired, Email, Length


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
    image = FileField('text')


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
    """Add a listing form."""

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

    image = MultipleFileField(
        render_kw={'multiple': True},
        validators=[InputRequired()],
        )


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

    image = MultipleFileField(
        render_kw={'multiple': True},
        validators=[InputRequired()],
        )


class ReserveListingForm(FlaskForm):
    """Reserve a listing form."""

    start_date = DateField(
        'Start Date',
        validators=[InputRequired()],
    )

    end_date = DateField(
        'End Date',
        validators=[InputRequired()],
    )


class ConfirmForm(FlaskForm):
    """Confirm a reservation form."""

    start_date = DateField(
        'Start Date',
        validators=[InputRequired()],
        render_kw={'readonly': True},
    )

    end_date = DateField(
        'End Date',
        validators=[InputRequired()],
        render_kw={'readonly': True},
    )

    total_cost = IntegerField(
        'Total Cost ($)',
        validators=[InputRequired()],
        render_kw={'readonly': True},
    )


class MessageForm(FlaskForm):
    """Form for sending a message"""
    content = TextAreaField('text', validators=[InputRequired()])


class CSRFForm (FlaskForm):
    """Form for CSRF validation only"""
