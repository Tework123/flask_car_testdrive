import datetime
import os

from flask import render_template, request, redirect, url_for, flash, make_response
from flask_paginate import get_page_parameter, Pagination
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Users, Brands, Cars, Photos, Reviews, ReviewsPhoto

from app.user import bp

from flask_login import current_user, login_user, logout_user, login_required

from app.user.forms import LoginForm, RegisterForm, ReviewsForm, EditProfile, PasswordSecurity

from app import login_manager

menu = [['Home', './'], ['Сar brands', 'show_brands'], ['Sing in', 'login'],
        ['Registration', 'register']]


@bp.route('/')
def index():
    whole_cars = db.session.query(Cars.name_car, db.func.min(Photos.name_photo), db.func.min(Photos.id_photo)).join(
        Photos,
        Cars.id_car == Photos.id_car).group_by(
        Cars.name_car).all()

    cars_dict = []
    for row in whole_cars:
        row = {'name_car': row.name_car, 'name_photo': row._data[1]}
        cars_dict.append(row)

    # может лучше сразу в базе весь путь к картинке хранить
    for car in cars_dict:
        car['name_photo'] = url_for('static', filename='car_image/' + car['name_photo'])

    return render_template('user/index.html', main_menu=menu, cars=cars_dict)


@bp.route('/show_brands', methods=['POST', 'GET'])
def show_brands():
    brands = db.session.query(Brands.name_brand, Brands.description, Brands.name_photo,
                              db.func.count(Cars.id_car)).join(Cars, Brands.id_brand == Cars.id_brand,
                                                               isouter=True).group_by(
        Brands.name_brand, Brands.description, Brands.name_photo).all()

    brands_dict = []
    for row in brands:
        row = {'name_brand': row.name_brand, 'description': row.description, 'name_photo': row.name_photo,
               'count_car': row._data[3]}
        brands_dict.append(row)

    for brand in brands_dict:
        brand['name_photo'] = url_for('static', filename='brand_image/' + brand['name_photo'])

    return render_template('user/show_brands.html', main_menu=menu, brands=brands_dict)


@bp.route('/show_brand_<alias>')
def show_brand(alias):
    try:
        brand = db.session.execute(db.select(Brands).filter_by(name_brand=alias)).scalar_one()
    except:
        return redirect(url_for('.show_brands'))
    try:

        cars = db.session.query(Cars.name_car, Cars.description, Photos.name_photo) \
            .join(Photos, Cars.id_car == Photos.id_car).join(
            Brands, Cars.id_brand == Brands.id_brand).where(Brands.name_brand == alias).all()

        cars_dict = [[]]
        first_car = cars[0][0]
        for row in cars:
            if row[0] == first_car:
                row = {'name_car': row.name_car, 'description': row.description, 'name_photo': row.name_photo}
                cars_dict[-1].append(row)
            else:
                first_car = row[0]

                row = {'name_car': row.name_car, 'description': row.description, 'name_photo': row.name_photo}
                cars_dict.append([row])

        for car in cars_dict:
            car[0]['description'] = car[0]['description'].split(', ')[0:3]
            for photo in car:
                photo['name_photo'] = url_for('static', filename='car_image/' + photo['name_photo'])

        brand.name_photo = url_for('static', filename='brand_image/' + brand.name_photo)

    except:
        cars_dict = []
        brand.name_photo = url_for('static', filename='brand_image/' + brand.name_photo)

    return render_template('user/show_brand.html', main_menu=menu, brand=brand, cars=cars_dict)


@bp.route('/show_car_<alias_car>')
def show_car(alias_car):
    car = db.session.query(Cars.name_car, Cars.description, Photos.name_photo, Brands.name_brand).join(Photos,
                                                                                                       Cars.id_car == Photos.id_car).join(
        Brands, Cars.id_brand == Brands.id_brand).where(Cars.name_car == alias_car).all()
    car_dict = []

    for row in car:
        row = {'name_car': row.name_car, 'description': row.description, 'name_photo': row.name_photo,
               'name_brand': row.name_brand}
        car_dict.append(row)

    for photo in car_dict:
        photo['name_photo'] = url_for('static', filename='car_image/' + photo['name_photo'])

    description = car_dict[0]['description'].split(', ')

    return render_template('user/show_car.html', main_menu=menu, car=car_dict,
                           description=description)


@bp.route('/add_review', methods=['POST', 'GET'])
@login_required
def add_review():
    form = ReviewsForm()
    name_car = request.args.get('add_car')

    review = db.session.query(Reviews.id_review).join(Cars, Reviews.id_car == Cars.id_car).where(
        Cars.name_car == name_car, Reviews.id_user == current_user.id_user).all()
    if len(review) >= 1:
        flash('You already add review for this car, you can change it', category='error')
        return redirect(url_for('.profile'))
        # перенаправить на его отзыв, а пока так

    if request.method == 'POST':
        if form.validate_on_submit():
            name_car = request.form['add_review']

            id_car = db.session.execute(db.select(Cars.id_car).filter_by(name_car=name_car)).scalar_one()
            review = Reviews(id_car=id_car, id_user=current_user.id_user, text=form.text.data, degree=form.degree.data,
                             date=datetime.datetime.now())
            db.session.add(review)
            db.session.flush()
            db.session.commit()

            id_review = db.session.execute(
                db.select(Reviews.id_review).filter_by(id_car=id_car, id_user=current_user.id_user)).scalar_one()

            # whole_photo = []
            #
            # for photo in form.photos.data:
            #     name_photo_db = ReviewsPhoto(id_review=id_review)
            #     whole_photo.append(name_photo_db)
            # print(whole_photo)
            # if len(whole_photo) > 1:
            #     db.session.add_all(whole_photo)
            #     db.session.flush()
            #     db.session.commit()
            #
            #     photos_id = db.session.execute(
            #         db.select(ReviewsPhoto.id_photo).filter_by(id_review=id_review)).scalars().all()
            #     print(photos_id)
            #     for photo_id in range(len(photos_id)):
            #         file_path = 'app/static/reviews_photo/' + str(photos_id[photo_id]) + '.jpg'
            #         if not os.path.exists(file_path):
            #             form.photos.data[photo_id].save(file_path)

            name_photo_db = ReviewsPhoto(id_review=id_review)
            db.session.add(name_photo_db)
            db.session.flush()
            db.session.commit()
            photo_id = db.session.execute(
                db.select(ReviewsPhoto.id_photo).filter_by(id_review=id_review)).scalars().first()
            file_path = 'app/static/reviews_photo/' + str(photo_id) + '.jpg'
            if not os.path.exists(file_path):
                form.photos.data.save(file_path)

            flash('Add review success', category='success')
            return redirect(url_for('.show_brands'))

    return render_template('user/add_review.html', main_menu=menu, form=form, car=name_car)


@bp.route('/show_reviews', methods=['POST', 'GET'])
def show_reviews():
    # try:
    page = request.args.get('page', 1, type=int)
    name_car = request.args.get('show_reviews')
    if request.method == 'POST':
        name_car = request.form['show_reviews']

    reviews = db.session.query(Reviews.text, Reviews.date, Reviews.degree, ReviewsPhoto.id_photo, Users.name).join(
        ReviewsPhoto, Reviews.id_review == ReviewsPhoto.id_review, isouter=True).join(Users,
                                                                                      Reviews.id_user == Users.id_user).where(
        Cars.name_car == name_car).order_by(Reviews.date.desc()).paginate(page=page, per_page=3, error_out=False)

    if reviews.has_next:
        next_url = url_for('user.show_reviews', page=reviews.next_num)
    else:
        next_url = None
    if reviews.has_prev:
        prev_url = url_for('user.show_reviews', page=reviews.prev_num)
    else:
        prev_url = None

    reviews_dict = [[]]

    if reviews.items != []:
        first_review = reviews.items[0][0]

        for row in reviews:

            if row[0] == first_review:
                row = {'text': row.text, 'date': row.date, 'degree': row.degree, 'id_photo': row.id_photo,
                       'name': row.name}
                reviews_dict[-1].append(row)
            else:
                first_review = row[0]
                row = {'text': row.text, 'date': row.date, 'degree': row.degree, 'id_photo': row.id_photo,
                       'name': row.name}
                reviews_dict.append([row])

        for review in reviews_dict:
            for photo in review:
                if photo['id_photo']:
                    photo['id_photo'] = url_for('static', filename='reviews_photo/' + str(photo['id_photo']) + '.jpg')
        # except:
        #     reviews_dict = []
    else:
        reviews_dict = []
    return render_template('user/show_reviews.html', main_menu=menu, reviews=reviews_dict, next_url=next_url,
                           prev_url=prev_url, name_car=name_car, title='Reviews')


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
                    flash('Ah shit, here we go again', category='success')
                    if form.remember.data:
                        login_user(user, remember=True, duration=datetime.timedelta(days=2))
                    else:
                        login_user(user)

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


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()


@login_manager.unauthorized_handler
def unauthorized():
    flash('Login for add review', category='error')
    return redirect(url_for('.login'))


@bp.route('/profile')
@login_required
def profile():
    image = current_user.profile_pic
    if not image:
        image = url_for('static', filename='profile_image/' + 'default.jpg')
    else:
        image = url_for('static', filename='profile_image/' + image)

    return render_template('user/profile.html', main_menu=menu, title='My profile', user=current_user,
                           profile_image=image)


# проверить, если чел сменит на емайл, который у кого то уже есть
# прикрутить посмотреть мой отзывы
# прикрутить заказы, просмотр заказов также нужен
# доделать админку
@bp.route('/edit_profile_<user>', methods=['GET', 'POST'])
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(user):
    form = EditProfile()
    if request.method == 'POST':
        if form.validate_on_submit():

            if form.password.data == form.repeat_password.data:

                try:
                    user = Users.query.filter_by(email=current_user.email).first()
                    hash = generate_password_hash(form.password.data)
                    user.name = form.name.data
                    user.password = hash
                    user.email = form.email.data
                    user.country = form.country.data

                    db.session.commit()
                    flash('Edit profile success', category='success')

                    return redirect(url_for('.profile'))

                except:
                    db.session.rollback()
                    flash('incorrect data', category='error')
            else:
                flash('incorrect repeat password', category='error')
        else:
            flash('This email already use', category='error')

    return render_template('user/edit_profile.html', main_menu=menu, title='Edit_profile', form=form)


@bp.route('/password_security', methods=['GET', 'POST'])
@login_required
def password_security():
    form = PasswordSecurity()

    if request.method == 'POST':
        print(form.password.data)

        if form.validate_on_submit():
            try:
                check_password = check_password_hash(current_user.password, form.password.data)
                if check_password:
                    flash('Ok', category='success')
                    return redirect(url_for('user.edit_profile', user=current_user.name))
                else:
                    flash('incorrect password', category='error')
            except:
                flash('incorrect password', category='error')

        else:
            flash('incorrect data', category='error')

    return render_template('user/password_security.html', form=form)


@bp.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']

        user = Users.query.filter_by(id_user=current_user.id_user).first()
        user.profile_pic = file.filename
        db.session.commit()

        file.save('app/static/profile_image/' + file.filename)
        # except:
        #     print('ошибка')
        return redirect(url_for('.profile'))
