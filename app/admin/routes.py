import os

from flask import render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.admin import bp
from app.admin.forms import LoginForm, AddBrand, AddCar
from app.models import Users, Brands, Cars, Photos, Reviews

menu = [['Home_users', '/'], ['Home', './'], ['Сar brands', 'show_brands'], ['Sing in', 'login'], ['Admin-panel', '#']]


# Обработка не найденных url через try except и перенаправление на показ брендов
#     хз еще как

@bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))

    return render_template('admin/index.html', main_menu=menu)


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
    brands = Brands.query.all()
    for brand in brands:
        brand.name_photo = url_for('static', filename='brand_image/' + brand.name_photo)

    return render_template('admin/show_brands.html', main_menu=menu, brands=brands)


@bp.route('/show_brand_<alias>')
def show_brand(alias):
    print('brand')
    if not isLogged():
        return redirect(url_for('.login'))
    # try:
    print(alias)
    brand = db.session.execute(db.select(Brands).filter_by(name_brand=alias)).scalar_one()
    # brand = db.sessionBrands.query.filter_by(name_brand=alias).first()

    print(brand)
    # except:
    #     return redirect(url_for('.show_brands'))
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
                brand = Brands(name_brand=form.name_brand.data, name_photo=brand_image)
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
            db_brand = Brands.query.filter_by(name_brand=name_brand).first()
            Brands.query.filter_by(name_brand=name_brand).delete()
            db.session.commit()

            file_path = 'app/static/brand_image/' + db_brand.name_photo
            if os.path.exists(file_path):
                os.remove(file_path)
            if db_brand:
                flash('Brand deleted', category='success')
            else:
                flash('brand not deleted', category='error')
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
        print(photo)
        photo['name_photo'] = url_for('static', filename='car_image/' + photo['name_photo'])

    # еще отзывы заджойнить

    return render_template('admin/show_car.html', main_menu=menu, car=car_dict, name_car=car_dict[0]['name_car'],
                           brand=car_dict[0]['name_brand'], description=car_dict[0]['description'])


@bp.route('/add_car', methods=['POST', 'GET'])
def add_car():
    form = AddCar()
    if request.method == 'GET':
        brand = request.args.get('add_car')

    if request.method == 'POST':
        brand = request.form['add_car']

        if form.validate_on_submit():
            # try:
            front_photo = request.files['front_photo']
            behind_photo = request.files['behind_photo']
            side_photo = request.files['side_photo']

            id_brand = db.session.execute(db.select(Brands.id_brand).filter_by(name_brand=brand)).scalar_one()
            car = Cars(name_car=form.name_car.data, description=form.description.data,
                       id_brand=id_brand)
            db.session.add(car)
            db.session.flush()
            db.session.commit()
            id_car = db.session.execute(db.select(Cars.id_car).filter_by(name_car=form.name_car.data)).scalar_one()

            photo_1 = Photos(id_car=id_car, name_photo=front_photo.filename)
            photo_2 = Photos(id_car=id_car, name_photo=behind_photo.filename)
            photo_3 = Photos(id_car=id_car, name_photo=side_photo.filename)
            db.session.add_all([photo_1, photo_2, photo_3])
            db.session.flush()
            db.session.commit()

            front_photo.save('app/static/car_image/' + front_photo.filename)
            behind_photo.save('app/static/car_image/' + behind_photo.filename)
            side_photo.save('app/static/car_image/' + side_photo.filename)

            flash('Add car success', category='success')

            return redirect(url_for('.show_brand', alias=brand))
    #
    #     except:
    #         db.session.rollback()
    #         flash('Add brand error', category='error')
    #
    # else:
    #     flash('incorrect file', category='error')

    return render_template('admin/add_car.html', main_menu=menu, title='Add car', form=form, brand=brand)


@bp.route('/delete_car', methods=['POST', 'GET'])
def delete_car():
    pass


@bp.route('/upload', methods=['POST', 'GET'])
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
