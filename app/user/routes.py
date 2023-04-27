from flask import render_template, request, redirect, url_for, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Users

from app.user import bp

from flask_login import current_user, login_user, logout_user, login_required

from app.user.forms import LoginForm, RegisterForm

menu = [['Home', '/'], ['Сar brands', 'car_brands'], ['Sing in', 'login'],
        ['Registration', 'register']]


@bp.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))

    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not Users.query.filter_by(email=form.email.data).first():

                if form.password.data == form.repeat_password.data:

                    try:
                        hash = generate_password_hash(form.password.data)
                        user = Users(name=form.name.data, password=hash, email=form.email.data,
                                     country=form.country.data)
                        db.session.add(user)
                        db.session.flush()
                        db.session.commit()
                        flash('Registration success', category='success')
                        new_user = Users.query.filter_by(email=form.email.data).first()
                        login_user(new_user)
                        flash('Welcome', category='success')

                        return redirect(url_for('.profile'))

                    except:
                        db.session.rollback()
                        flash('incorrect data', category='error')
                else:
                    flash('incorrect repeat password', category='error')
            else:
                flash('This email already use', category='error')


        else:
            flash('incorrect data', category='error')

    return render_template('user/register.html', main_menu=menu, form=form)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.profile'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = Users.query.filter_by(email=form.email.data).first()
                check_password = check_password_hash(user.password, form.password.data)
                if check_password:
                    login_user(user)
                    flash('Ah shit, here we go again', category='success')
                    return redirect(url_for('.profile'))
                else:
                    flash('incorrect password', category='error')
            except:
                flash('No such user', category='error')

        else:
            flash('incorrect data', category='error')

    return render_template('user/login.html', main_menu=menu, title='Sing in', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@bp.route('/profile')
def profile():
    image = current_user.profile_pic
    if not image:
        image = url_for('static', filename='profile_image/' + 'default.jpg')
    else:
        image = url_for('static', filename='profile_image/' + image)
    return render_template('user/profile.html', main_menu=menu, title='My profile', user=current_user,
                           profile_image=image)


@bp.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        user = Users.query.filter_by(id_user=current_user.id_user).first()
        user.profile_pic = file.filename
        db.session.commit()

        file.save('app/static/profile_image/' + file.filename)
        # except:
        #     print('ошибка')
        return redirect(url_for('.profile'))

    #
    # hash = generate_password_hash(form.password.data)
    # user = Users(name=form.name.data, password=hash, email=form.email.data, country=form.country.data)
    # db.session.add(user)
    # db.session.flush()
    # db.session.commit()
    #
