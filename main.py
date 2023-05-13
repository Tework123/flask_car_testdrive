from flask_mail import Message

from app import app, mail
from flask import url_for, redirect
from app import db
import logging

from config import Config

menu = [['Home', '/user'], ['Сar brands', '/user/show_brands'], ['Sing in', '/user/login'],
        ['Registration', '/user/register']]


@app.route('/')
def index():

    msg = Message('mail title', sender=Config.MAIL_USERNAME,
                  recipients=[Config.ADMINS])
    msg.body = 'Body of the email to send'
    mail.send(msg)

    return redirect(url_for('user.index'))


if __name__ == '__main__':
    with app.app_context():
        # импорт и регистрация blueprint
        from app.user import bp as bp_user

        app.register_blueprint(bp_user, url_prefix='/user')

        from app.admin import bp as bp_admin

        app.register_blueprint(bp_admin, url_prefix='/admin')
        db.drop_all()
        db.create_all()

    app.run(debug=True)
