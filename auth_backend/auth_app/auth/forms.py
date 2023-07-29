from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, \
    MultipleFileField, FileField, DateField
from wtforms.validators import Email, DataRequired, Length, NumberRange, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Sing in')


class RegisterForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email: ', validators=[Email()])
    phone = StringField('Phone: ', validators=[DataRequired(), Length(min=5, max=40)])
    country = StringField('Country: ', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=30)])
    repeat_password = PasswordField('Repeat password: ',
                                    validators=[DataRequired(), EqualTo('password', message='password must match'),
                                                Length(min=4, max=30)])


class ResetPassword(FlaskForm):
    email = StringField('Your email: ', validators=[DataRequired(), Email()])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=4, max=330)])
    repeat_password = PasswordField('Repeat password: ', validators=[DataRequired(), Length(min=4, max=330)])
