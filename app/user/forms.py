from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Sing in')


class RegisterForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email: ', validators=[Email()])
    country = StringField('Country: ', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=330)])
    repeat_password = PasswordField('Repeat password: ', validators=[DataRequired(), Length(min=4, max=330)])
    submit = SubmitField('Register')
