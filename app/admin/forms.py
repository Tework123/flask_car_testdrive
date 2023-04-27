from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import Email, DataRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField('Sing in')


class AddBrand(FlaskForm):
    name_brand = StringField('Name brand: ', validators=[DataRequired(), Length(min=2, max=100)])
    photo = FileField('Photo: ')
    submit = SubmitField('Add brand')


class AddCar(FlaskForm):
    name_car = StringField('Name car: ', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description: ', validators=[DataRequired(), Length(min=2, max=100)])
    front_photo = FileField('Front photo: ')
    behind_photo = FileField('Behind photo: ')
    side_photo = FileField('Side photo: ')
    submit = SubmitField('Add car')
