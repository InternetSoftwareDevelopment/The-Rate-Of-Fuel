from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, IntegerField, FloatField, DateField, DecimalField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import Client

# Client Quote form
class Quote(FlaskForm):
    gallons_requested = IntegerField('Gallons Requested', validators=[DataRequired()])
    delivery_date = DateField('Delivery Date', format='%m/%d/%Y', validators=[DataRequired()])
    request_date = DateField('Request Date', format='%m/%d/%Y', validators=[DataRequired()])
    delivery_address = StringField('Delivery Address', validators=[DataRequired()])
    delivery_city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    delivery_state = StringField('State', validators=[DataRequired(), Length(min=2, max=2)])
    delivery_zip = StringField('Zip', validators=[DataRequired(), Length(min=5, max=10)])
    delivery_contact_name = StringField('Delivery Contact Name', validators=[DataRequired()])
    delivery_contact_phone = StringField('Delivery Contact Phone', validators=[DataRequired()])
    delivery_contact_email = StringField('Delivery Contact Email', validators=[DataRequired(), Email()])
    suggested_price = FloatField('Suggested Price')
    total_amount_due = FloatField('Total Amount Due')
    submit = SubmitField('Submit')


# Client registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=2)])
    zip = StringField('Zip', validators=[DataRequired(), Length(min=5, max=10)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        client = Client.query.filter_by(username=username.data).first()
        if client:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        client = Client.query.filter_by(email=email.data).first()
        if client:
            raise ValidationError('This email seems be associated with an existing account. Please check again.')

# Client Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# Update Account Form
class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_name(self, name):
        if name.data != current_user.name:
            client = Client.query.filter_by(name=name.data).first()
            if client:
                raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            client = Client.query.filter_by(email=email.data).first()
            if client:
                raise ValidationError('This email seems be associated with an existing account. Please check again.')

    def validate_address(self, address):
        if address.data != current_user.address:
            client = Client.query.filter_by(address=address.data).first()
            if client:
                raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            client = Client.query.filter_by(phone=phone.data).first()
            if client:
                raise ValidationError('This username is already taken. Please choose a different one.')