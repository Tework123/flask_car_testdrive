import os

from flask import render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.admin import bp
from app.admin.forms import LoginForm, AddBrand, AddCar
from app.models import Users, Brands, Cars, Photos, Reviews, ReviewsPhoto

menu = [['Home_users', '/'], ['Home', './'], ['Сar brands', 'show_brands'], ['Sing in', 'login'], ['Admin-panel', '#']]


@bp.route('/')
def index():
    if not is_logged():
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


@bp.route('/show_brands', methods=['POST', 'GET'])
def show_brands():
    if not is_logged():
        return redirect(url_for('.login'))
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

    return render_template('admin/show_brands.html', main_menu=menu, brands=brands_dict)


@bp.route('/show_brand_<alias>')
def show_brand(alias):
    if not is_logged():
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

        brand.name_photo = url_for('static', filename='brand_image/' + brand.name_photo)

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
                brand = Brands(name_brand=form.name_brand.data, name_photo=brand_image,
                               description=form.description.data)
                db.session.add(brand)
                db.session.flush()
                db.session.commit()
                file_path = 'app/static/brand_image/' + brand_image
                if not os.path.exists(file_path):
                    file.save(file_path)
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
            if brand:
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
            return redirect('.show_brands')

    return redirect(url_for('.show_brands'))


@bp.route('/show_car_<alias_car>')
def show_car(alias_car):
    if not is_logged():
        return redirect(url_for('.login'))
    car = db.session.query(Cars.name_car, Cars.description, Cars.url_video, Photos.name_photo, Brands.name_brand).join(
        Photos,
        Cars.id_car == Photos.id_car).join(
        Brands, Cars.id_brand == Brands.id_brand).where(Cars.name_car == alias_car).all()
    car_dict = []

    for row in car:
        row = {'name_car': row.name_car, 'description': row.description, 'url_video': row.url_video,
               'name_photo': row.name_photo,
               'name_brand': row.name_brand}
        car_dict.append(row)

    for photo in car_dict:
        photo['name_photo'] = url_for('static', filename='car_image/' + photo['name_photo'])

    description = car_dict[0]['description'].split(', ')

    car_video = car_dict[0]['url_video'].split()
    car_video = car_video[3][5:-1]

    return render_template('admin/show_car.html', main_menu=menu, car=car_dict,
                           description=description, car_video=car_video)


@bp.route('/show_reviews', methods=['POST', 'GET'])
def show_reviews():
    # try:
    page = request.args.get('page', 1, type=int)
    name_car = request.args.get('show_reviews')
    if request.method == 'POST':
        name_car = request.form['show_reviews']

    reviews = db.session.query(Reviews.id_review, Reviews.text, Reviews.date, Reviews.degree, ReviewsPhoto.id_photo,
                               Users.name).join(
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

    if reviews.items:
        first_review = reviews.items[0][0]

        for row in reviews:

            if row[0] == first_review:
                row = {'id_review': row.id_review, 'text': row.text, 'date': row.date, 'degree': row.degree,
                       'id_photo': row.id_photo,
                       'name': row.name}
                reviews_dict[-1].append(row)
            else:
                first_review = row[0]
                row = {'id_review': row.id_review, 'text': row.text, 'date': row.date, 'degree': row.degree,
                       'id_photo': row.id_photo,
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
    return render_template('admin/show_reviews.html', main_menu=menu, reviews=reviews_dict, next_url=next_url,
                           prev_url=prev_url, name_car=name_car, title='Reviews')


@bp.route('/delete_review', methods=['POST', 'GET'])
def delete_review():
    if request.method == 'POST':
        id_review = request.form['delete_review']
        try:
            id_photo = db.session.execute(db.select(ReviewsPhoto.id_photo).filter_by(id_review=id_review)).scalar_one()
            if id_photo is not None:

                file_path = 'app/static/reviews_photo/' + str(id_photo) + '.jpg'
                if os.path.exists(file_path):
                    os.remove(file_path)

                Reviews.query.filter_by(id_review=id_review).delete()
                db.session.commit()
                flash('review deleted', category='success')
            else:
                Reviews.query.filter_by(id_review=id_review).delete()
                db.session.commit()
                flash('review deleted', category='success')

        except:
            flash('Error, review not deleted', category='error')

    return redirect(url_for('.show_brands'))


@bp.route('/add_car', methods=['POST', 'GET'])
def add_car():
    form = AddCar()
    if request.method == 'GET':
        brand = request.args.get('add_car')

    if request.method == 'POST':
        brand = request.form['add_car']

        if form.validate_on_submit():
            # try:
            id_brand = db.session.execute(db.select(Brands.id_brand).filter_by(name_brand=brand)).scalar_one()
            car = Cars(name_car=form.name_car.data, description=form.description.data,
                       id_brand=id_brand, url_video=form.url_video.data)

            db.session.add(car)
            db.session.flush()
            db.session.commit()
            id_car = db.session.execute(db.select(Cars.id_car).filter_by(name_car=form.name_car.data)).scalar_one()
            whole_photo = []
            for photo in form.photos.data:
                name_photo_str = photo.filename
                name_photo_db = Photos(id_car=id_car, name_photo=photo.filename)
                whole_photo.append(name_photo_db)
                file_path = 'app/static/car_image/' + name_photo_str
                if not os.path.exists(file_path):
                    photo.save(file_path)

            db.session.add_all(whole_photo)
            db.session.flush()
            db.session.commit()

            flash('Add car success', category='success')
            return redirect(url_for('.show_brand', alias=brand))

        # except:
        #     db.session.rollback()
        #     flash('Add car error', category='error')

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


def is_logged():
    return True if session.get('admin_logged') else False


def login_admin():
    session['admin_logged'] = 1


def logout_admin():
    session.pop('admin_logged', None)


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if is_logged():
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


@bp.route('/logout')
def logout():
    if not is_logged():
        return redirect(url_for('.login'))

    logout_admin()
    return redirect(url_for('.login'))


@bp.route('/profile')
def profile():
    return render_template('admin/profile.html', main_menu=menu, title='My admin profile', user='admin',
                           email='admin@admin.com')
