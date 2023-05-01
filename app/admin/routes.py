import os

from flask import render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.admin import bp
from app.admin.forms import LoginForm, AddBrand, AddCar
from app.models import Users, Brands, Cars, Photos

menu = [['Home_users', '/'], ['Home', './'], ['Сar brands', 'show_brands'], ['Sing in', 'login'], ['Admin-panel', '#']]


# Обработка не найденных url через try except и перенаправление на показ брендов
#     хз еще как

@bp.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))

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

    return render_template('admin/index.html', main_menu=menu, cars=cars_dict)


def isLogged():
    return True if session.get('admin_logged') else False


def login_admin():
    session['admin_logged'] = 1


def logout_admin():
    session.pop('admin_logged', None)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if isLogged():
        return redirect(url_for('.profile'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                email = form.email.data
                password = form.password.data
                if email == 'admin@admin.com' and password == 'admin':
                    login_admin()
                    flash('Ah shit, here we go again. Admin', category='success')
                    return redirect(url_for('.profile'))
                else:
                    flash('incorrect password or email', category='error')
            except:
                flash('No such user', category='error')

        else:
            flash('incorrect data', category='error')

    return render_template('admin/login.html', main_menu=menu, title='Sing in', form=form)


@bp.route('/show_brands', methods=['POST', 'GET'])
def show_brands():
    if not isLogged():
        return redirect(url_for('.login'))
    brands = db.session.query(Brands.name_brand, Brands.description, Brands.name_photo,
                              db.func.count(Cars.id_car)).join(Cars, Brands.id_brand == Cars.id_brand, isouter=True).group_by(
                                  Brands.name_brand, Brands.description, Brands.name_photo).all()
    print(brands)
    # распарсить и добавить количество машинок присутствующих

    for brand in brands:
        brand.name_photo = url_for('static', filename='brand_image/' + brand.name_photo)

    return render_template('admin/show_brands.html', main_menu=menu, brands=brands)


@bp.route('/show_brand_<alias>')
def show_brand(alias):
    if not isLogged():
        return redirect(url_for('.login'))
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

    except:
        cars_dict = []
    brand.name_photo = url_for('static', filename='brand_image/' + brand.name_photo)

    return render_template('admin/show_brand.html', main_menu=menu, brand=brand, cars=cars_dict)


@bp.route('/add_brand', methods=['POST', 'GET'])
def add_brand():
    form = AddBrand()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = request.files['photo']
            brand_image = file.filename

            try:
                brand = Brands(name_brand=form.name_brand.data, name_photo=brand_image, description=form.description.data)
                db.session.add(brand)
                db.session.flush()
                db.session.commit()

                file.save('app/static/brand_image/' + brand_image)
                flash('Add brand success', category='success')

                return redirect(url_for('.show_brands'))

            except:
                db.session.rollback()
                flash('Add brand error', category='error')

        else:
            flash('incorrect file', category='error')

    return render_template('admin/add_brand.html', main_menu=menu, form=form, title='Add brand')


@bp.route('/delete_brand', methods=['POST', 'GET'])
def delete_brand():
    if request.method == 'POST':
        try:
            name_brand = request.form['delete_brand']

            brand = db.session.query(Cars.name_car, Brands.name_photo, Photos.name_photo).join(Brands,
                                                                                               Cars.id_brand == Brands.id_brand).join(
                Photos, Cars.id_car == Photos.id_car).where(Brands.name_brand == name_brand).all()
            if brand != []:
                brand_photo = brand[0][1]

                photos_dict = []
                for row in brand:
                    row = {'name_photo': row.name_photo}
                    photos_dict.append(row)

                for photo in photos_dict:
                    file_path = 'app/static/car_image/' + photo['name_photo']
                    if os.path.exists(file_path):
                        os.remove(file_path)

                file_path = 'app/static/brand_image/' + brand_photo
                if os.path.exists(file_path):
                    os.remove(file_path)

                Brands.query.filter_by(name_brand=name_brand).delete()

                db.session.commit()

                flash('brand deleted', category='success')
            else:

                brand_photo = db.session.execute(
                    db.select(Brands.name_photo).filter_by(name_brand=name_brand)).scalar_one()
                Brands.query.filter_by(name_brand=name_brand).delete()
                db.session.commit()

                file_path = 'app/static/brand_image/' + brand_photo
                if os.path.exists(file_path):
                    os.remove(file_path)
                flash('brand deleted', category='success')



        except:
            flash('Error, brand not deleted', category='error')

    return redirect(url_for('.show_brands'))


@bp.route('/show_car_<alias_car>')
def show_car(alias_car):
    car = db.session.query(Cars.name_car, Cars.description, Photos.name_photo, Brands.name_brand).join(Photos,
                                                                                                       Cars.id_car == Photos.id_car).join(
        Brands, Cars.id_brand == Brands.id_brand).where(Cars.name_car == alias_car).all()
    car_dict = []

    # reviews = db.session.query(Reviews.text, Reviews.degree, Reviews.date, Users.name).join(
    #     Reviews.id_car == Cars.id_car).join(Reviews.id_user == Users.id_user).where(Cars.name_car == alias_car).all()

    for row in car:
        row = {'name_car': row.name_car, 'description': row.description, 'name_photo': row.name_photo,
               'name_brand': row.name_brand}
        car_dict.append(row)

    # for row in reviews:
    #     print(row)

    for photo in car_dict:
        photo['name_photo'] = url_for('static', filename='car_image/' + photo['name_photo'])

    description = car_dict[0]['description'].split(', ')

    # еще отзывы заджойнить

    return render_template('admin/show_car.html', main_menu=menu, car=car_dict, name_car=car_dict[0]['name_car'],
                           brand=car_dict[0]['name_brand'], description=description)


@bp.route('/add_car', methods=['POST', 'GET'])
def add_car():
    form = AddCar()
    if request.method == 'GET':
        brand = request.args.get('add_car')

    if request.method == 'POST':
        brand = request.form['add_car']

        if form.validate_on_submit():
            try:
                id_brand = db.session.execute(db.select(Brands.id_brand).filter_by(name_brand=brand)).scalar_one()
                car = Cars(name_car=form.name_car.data, description=form.description.data,
                           id_brand=id_brand)
                db.session.add(car)
                db.session.flush()
                db.session.commit()
                id_car = db.session.execute(db.select(Cars.id_car).filter_by(name_car=form.name_car.data)).scalar_one()
                whole_photo = []
                for photo in form.photos.data:
                    name_photo_str = photo.filename
                    name_photo_db = Photos(id_car=id_car, name_photo=photo.filename)
                    whole_photo.append(name_photo_db)
                    photo.save('app/static/car_image/' + name_photo_str)

                db.session.add_all(whole_photo)
                db.session.flush()
                db.session.commit()

                flash('Add car success', category='success')
                return redirect(url_for('.show_brand', alias=brand))

            except:
                db.session.rollback()
                flash('Add brand error', category='error')

        else:
            flash('incorrect file', category='error')

    return render_template('admin/add_car.html', main_menu=menu, title='Add car', form=form, brand=brand)


@bp.route('/delete_car', methods=['POST', 'GET'])
def delete_car():
    if request.method == 'POST':
        try:
            name_car = request.form['delete_car']

            car_and_photos = db.session.query(Photos.name_photo) \
                .join(Cars, Cars.id_car == Photos.id_car).where(Cars.name_car == name_car).all()

            car_and_photos_dict = []
            for row in car_and_photos:
                row = {'name_photo': row.name_photo}
                car_and_photos_dict.append(row)

            for dict in car_and_photos_dict:
                file_path = 'app/static/car_image/' + dict['name_photo']
                if os.path.exists(file_path):
                    os.remove(file_path)

            Cars.query.filter_by(name_car=name_car).delete()
            db.session.commit()
            flash('car deleted', category='success')

        except:
            flash('Error, car not deleted', category='error')

    return redirect(url_for('.show_brands'))


@bp.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        user = Users.query.filter_by(id_user=current_user.id_user).first()
        user.profile_pic = file.filename
        db.session.commit()
        file.save('app/static/profile_image/' + file.filename)

        return redirect(url_for('.profile'))


@bp.route('/logout')
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()
    return redirect(url_for('.login'))


@bp.route('/profile')
def profile():
    if not isLogged():
        return redirect(url_for('.login'))

    return render_template('admin/profile.html', main_menu=menu, title='My admin profile', user='admin',
                           email='admin@admin.com')
