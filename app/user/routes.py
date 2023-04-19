from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
# from flask import Blueprint

from app import db
from app.models import Users, MainMenu

from app.user import bp

from flask_login import current_user, login_user

from app.user.forms import LoginForm, RegisterForm


# from app.user.user_login import User_login


# @bp.route('/', methods=['POST', 'GET'])
# def index():
#     return 'user'


@bp.route('/profile')
def profile():
    return 'user profile'


@bp.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    print('ok1')
    if form.validate_on_submit():
        # if request.method == 'POST':
        # try:
        print('ok2')
        hash = generate_password_hash(form.password.data)
        user = Users(name=form.name.data, password=hash, email=form.email.data, country=form.country.data)
        print('ok3')
        db.session.add(user)
        db.session.flush()
        db.session.commit()
    # except:
    #     db.session.rollback()
    #     print('Ошибка добавления в бд')

    # return redirect(url_for('profile'))

    main_menu = MainMenu.query.all()
    return render_template('register.html', main_menu=main_menu, form=form)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        print(current_user)
        return redirect(url_for('profile'))
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            print('POST')
            # try:
            user = Users.query.filter_by(email=request.form['email']).first()
            # user = Users(user)
            if user:
                # user = Users().create(user)
                # u_login = User_login().create(user)

                # прочитать перевод книжки, нихрена не понятно, найти у него эти базы данных
                # как он создает экземпляры
                login_user(user)
                print(user.email)
                return redirect(url_for('user.profile'))
            else:
                print('Ошибка авторизации')
            # flash('error')

    main_menu = MainMenu.query.all()
    return render_template('login.html', main_menu=main_menu, title='Sing in', form=form)
