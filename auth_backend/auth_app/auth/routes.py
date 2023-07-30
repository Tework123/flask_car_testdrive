import datetime
import json

from flask import redirect, url_for, request, flash, render_template, jsonify
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

# from auth_backend.auth_app
from auth_app import db
from auth_app.models import Users
from auth_app.auth import bp, menu
from auth_app.auth.forms import LoginForm, RegisterForm


# refactor
@bp.route('/register', methods=['POST', 'GET'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('.profile'))

    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not Users.query.filter_by(email=form.email.data).first():

                hash = generate_password_hash(form.password.data)
                # try:
                user = Users(name=form.name.data, password=hash, email=form.email.data,
                                 country=form.country.data, phone=form.phone.data)
                db.session.add(user)
                db.session.flush()
                db.session.commit()
                # except Exception as e:
                #     raise Exception
                    # raise HtmlDbError('register bd error', str(e), 500)

                # db.session.rollback()

                flash('Registration success', category='success')
                flash('Welcome', category='success')

                subject = 'You was register on testdrive'
                # body = current_user.name + ' Welcome!'
                # send_email(subject, CONFIG.MAIL_USERNAME, [current_user.email], body)

                # return redirect(url_for('.profile'))
                return redirect('http://127.0.0.1:5000/', code=301)


            else:
                flash('This email already use', category='error')

    return render_template('auth/register.html', main_menu=menu, form=form)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('.profile'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = Users.query.filter_by(email=form.email.data).first()
                check_password = check_password_hash(user.password, form.password.data)
                if check_password:
                    flash('Ah shit, here we go again', category='success')
                    if form.remember.data:
                        login_user(user, remember=True, duration=datetime.timedelta(days=30))
                    else:
                        login_user(user)

                    return redirect('http://127.0.0.1:5000/', code=301)

                    # return redirect(url_for('.profile'))
                else:
                    flash('incorrect password', category='error')
            except:
                flash('No such user', category='error')

        else:
            flash('incorrect data', category='error')

    return render_template('auth/login.html', main_menu=menu, title='Sing in', form=form)


from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


from sqlalchemy.ext.serializer import loads, dumps


@bp.route('/get_user/<id>', methods=['GET'])
def get_user(id):
    response = Users.query.get(int(id))

    response = json.dumps(response, cls=AlchemyEncoder)

    return jsonify({'object': response})
