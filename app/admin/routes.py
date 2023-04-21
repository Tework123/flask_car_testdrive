from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from app.admin import bp
from app.admin.forms import LoginForm
from app.models import Users

menu = [['Home_users', '/'], ['Home', './'], ['Сar brands', 'car_brands'], ['Sing in', 'login'], ['Admin-panel', '#']]


@bp.route('/')
def index():
    return render_template('admin/index.html', main_menu=menu)


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

    return render_template('admin/login.html', main_menu=menu, title='Sing in', form=form)


@bp.route('/car_brands', methods=['POST', 'GET'])
def show_car_brands():
    return render_template('admin/car_brands.html', main_menu=menu)


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
    return render_template('admin/profile.html', main_menu=menu, title='My profile', user=current_user,
                           profile_image=image)
