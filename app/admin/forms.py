from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, MultipleFileField
from wtforms.validators import Email, DataRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=100)])


class AddBrand(FlaskForm):
    name_brand = StringField('Name brand: ', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description: ')
    photo = FileField('Photo: ')


class AddCar(FlaskForm):
    name_car = StringField('Name car: ', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description: ', validators=[DataRequired(), Length(min=2, max=100)])
    photos = MultipleFileField('Photos: ')
