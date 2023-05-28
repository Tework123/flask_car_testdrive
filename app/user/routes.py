import datetime
import json
import time
from datetime import datetime as datetime_module
import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, redis
from app.user.forms import TakeTestdrive, MessagesForm
from app.models import Users, Brands, Cars, Photos, Reviews, ReviewsPhoto, TestDrive, ResetPasswordStatic, Messages

from app.user import bp

from flask_login import current_user, login_user, logout_user, login_required

from app.user.email import send_password_reset_email, send_email, add_to_queue_send_email, send_test
from app.user.forms import LoginForm, RegisterForm, ReviewsForm, EditProfile, PasswordSecurity, ResetPassword, \
    ResetPasswordForm

from app import login_manager
from flask_car_testdrive import CONFIG

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
    try:
        car_video = car_dict[0]['url_video'].split()
        car_video = car_video[3][5:-1]
    except:
        car_video = 'Not video'

    return render_template('user/show_car.html', main_menu=menu, car=car_dict,
                           description=description, car_video=car_video)


@bp.route('/add_review', methods=['POST', 'GET'])
@login_required
def add_review():
    # add only jpg
    form = ReviewsForm()
    name_car = request.args.get('add_car')

    review = db.session.query(Reviews.id_review).join(Cars, Reviews.id_car == Cars.id_car).where(
        Cars.name_car == name_car, Reviews.id_user == current_user.id_user).all()
    if len(review) >= 1:
        flash('You already add review for this car, you can change it', category='error')
        return redirect(url_for('.show_my_reviews'))

    if request.method == 'POST':
        if form.validate_on_submit():
            name_car = request.form['add_review']

            id_car = db.session.execute(db.select(Cars.id_car).filter_by(name_car=name_car)).scalar_one()
            review = Reviews(id_car=id_car, id_user=current_user.id_user, text=form.text.data, degree=form.degree.data,
                             date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(review)
            db.session.flush()
            db.session.commit()

            if form.photos.data.filename:
                id_review = db.session.execute(
                    db.select(Reviews.id_review).filter_by(id_car=id_car, id_user=current_user.id_user)).scalar_one()

                name_photo_db = ReviewsPhoto(id_review=id_review)
                db.session.add(name_photo_db)
                db.session.flush()
                db.session.commit()
                photo_id = db.session.execute(
                    db.select(ReviewsPhoto.id_photo).filter_by(id_review=id_review)).scalars().first()
                file_path = CONFIG.basepath + 'app/static/reviews_photo/' + str(photo_id) + '.jpg'
                if not os.path.exists(file_path):
                    form.photos.data.save(file_path)

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
            #         file_path = Config.basepath + 'app/static/reviews_photo/' + str(photos_id[photo_id]) + '.jpg'
            #         if not os.path.exists(file_path):
            #             form.photos.data[photo_id].save(file_path)

            flash('Add review success', category='success')
            return redirect(url_for('.show_brands'))

    return render_template('user/add_review.html', main_menu=menu, form=form, car=name_car)


@bp.route('/show_reviews', methods=['POST', 'GET'])
def show_reviews():
    try:
        page = request.args.get('page', 1, type=int)
        name_car = request.args.get('show_reviews')
        if request.method == 'POST':
            name_car = request.form['show_reviews']

        reviews = db.session.query(Reviews.text, Reviews.date, Reviews.degree, ReviewsPhoto.id_photo, Users.name,
                                   Users.id_user).join(
            ReviewsPhoto, Reviews.id_review == ReviewsPhoto.id_review, isouter=True).join(Users,
                                                                                          Reviews.id_user == Users.id_user).where(
            Cars.name_car == name_car).order_by(Reviews.date.desc()).paginate(page=page, per_page=2, error_out=False)

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
                           'name': row.name, 'id_user': row.id_user}
                    reviews_dict[-1].append(row)
                else:
                    first_review = row[0]
                    row = {'text': row.text, 'date': row.date, 'degree': row.degree, 'id_photo': row.id_photo,
                           'name': row.name, 'id_user': row.id_user}
                    reviews_dict.append([row])

            for review in reviews_dict:
                for photo in review:
                    if photo['id_photo']:
                        photo['id_photo'] = url_for('static',
                                                    filename='reviews_photo/' + str(photo['id_photo']) + '.jpg')
                        print(photo['id_photo'])
        else:
            reviews_dict = []

    except:
        reviews_dict = []
    return render_template('user/show_reviews.html', main_menu=menu, reviews=reviews_dict, next_url=next_url,
                           prev_url=prev_url, name_car=name_car, title='Reviews')


@bp.route('/show_my_reviews', methods=['POST', 'GET'])
@login_required
def show_my_reviews():
    try:
        my_reviews = db.session.query(Reviews.id_review, Reviews.date, Reviews.text, Reviews.degree, Cars.name_car,
                                      ReviewsPhoto.id_photo).join(ReviewsPhoto,
                                                                  Reviews.id_review == ReviewsPhoto.id_review,
                                                                  isouter=True).where(
            Reviews.id_user == current_user.id_user).all()

        if my_reviews:
            my_reviews_dict = []

            for row in my_reviews:
                row = {'id_review': row.id_review, 'date': row.date, 'text': row.text, 'degree': row.degree,
                       'id_photo': row.id_photo, 'name_car': row.name_car}
                my_reviews_dict.append(row)

            for review in my_reviews_dict:
                if review['id_photo']:
                    review['id_photo'] = url_for('static', filename='reviews_photo/' + str(review['id_photo']) + '.jpg')
        else:
            my_reviews_dict = []
    except:
        flash('Don`t have your reviews now', category='error')
        my_reviews_dict = []
    return render_template('user/show_my_reviews.html', main_menu=menu, title='My reviews', my_reviews=my_reviews_dict)


@bp.route('/delete_review', methods=['POST', 'GET'])
def delete_review():
    if request.method == 'POST':
        id_review = request.form['delete_review']
        try:
            id_photo = db.session.execute(db.select(ReviewsPhoto.id_photo).filter_by(id_review=id_review)).scalar_one()
            if id_photo is not None:

                file_path = CONFIG.basepath + 'app/static/reviews_photo/' + str(id_photo) + '.jpg'
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

    return redirect(url_for('.show_my_reviews'))


@bp.route('/add_message', methods=['POST', 'GET'])
def add_message():
    form = MessagesForm()
    email = request.args.get('add_message')
    print(email)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form['add_message']
            id_user = db.session.execute(db.select(Users.id_user).filter_by(email=email)).scalar_one()
            print(id_user)
            message = Messages(text=form.text.data, id_sender=current_user.id_user, id_recipient=id_user)
            db.session.add(message)
            db.session.flush()
            db.session.commit()
            flash('Message send success', category='success')
            return redirect(url_for('.profile'))

    return render_template('user/add_message.html', main_menu=menu, title='Add message', form=form, email=email)


@bp.route('/show_my_messages', methods=['POST', 'GET'])
def show_my_messages():
    # try:
    user = Users.query.filter_by(id_user=current_user.id_user).first()
    user.last_seen_profile = datetime.datetime.now()
    db.session.commit()

    page = request.args.get('page', 1, type=int)

    my_messages = db.session.query(Messages.text, Messages.date, Messages.id_sender, Users.name
                                   ).join(Users,
                                          Messages.id_sender == Users.id_user).where(
        Messages.id_recipient == current_user.id_user).order_by(Messages.date.desc()).paginate(page=page,
                                                                                               per_page=2,
                                                                                               error_out=False)
    if my_messages.has_next:
        next_url = url_for('user.show_my_messages', page=my_messages.next_num)
    else:
        next_url = None
    if my_messages.has_prev:
        prev_url = url_for('user.show_my_messages', page=my_messages.prev_num)
    else:
        prev_url = None

    my_messages_dict = []

    if my_messages.items != []:
        for row in my_messages:
            row = {'text': row.text, 'date': row.date,
                   'name': row.name, 'id_sender': row.id_sender}
            my_messages_dict.append(row)

    else:
        my_messages_dict = []
    print(my_messages_dict)
    # except:
    # reviews_dict = []
    return render_template('user/show_my_messages.html', main_menu=menu, my_messages=my_messages_dict,
                           next_url=next_url,
                           prev_url=prev_url, title='My messages')


@bp.route('/show_my_test_drives', methods=['POST', 'GET'])
def show_my_test_drives():
    try:
        my_test_drives = db.session.query(TestDrive.id_order, TestDrive.price, TestDrive.date_start, TestDrive.date_end,
                                          Cars.name_car,
                                          db.func.min(Photos.name_photo)).join(Cars,
                                                                               TestDrive.id_car == Cars.id_car).join(
            Photos, Cars.id_car == Photos.id_car).where(
            TestDrive.id_user == current_user.id_user).group_by(TestDrive.id_order, TestDrive.price,
                                                                TestDrive.date_start,
                                                                TestDrive.date_end,
                                                                Cars.name_car).order_by(
            TestDrive.date_start.desc()).all()

        if my_test_drives:
            my_test_drives_dict = []
            for row in my_test_drives:
                row = {'id_order': row.id_order, 'price': row.price, 'date_start': row.date_start,
                       'date_end': row.date_end,
                       'name_car': row.name_car,
                       'name_photo': row._data[5]}
                my_test_drives_dict.append(row)

            for test_drive in my_test_drives_dict:
                if test_drive['name_photo']:
                    test_drive['name_photo'] = url_for('static', filename='car_image/' + test_drive['name_photo'])

            time_now = datetime.datetime.now()
        else:
            time_now = datetime.datetime.now()
            my_test_drives_dict = []
    except:
        flash('Don`t have your test_drive now', category='error')
        my_test_drives_dict = []

    return render_template('user/show_my_test_drives.html', main_menu=menu, my_test_drives=my_test_drives_dict,
                           time_now=time_now)


@bp.route('/delete_test_drive', methods=['POST', 'GET'])
def delete_test_drive():
    if request.method == 'POST':
        id_order = request.form['delete_test_drive']
        try:
            TestDrive.query.filter_by(id_order=id_order).delete()
            db.session.commit()
            flash('test drive deleted', category='success')

        except:
            flash('Error, test drive not deleted', category='error')
    return redirect(url_for('.show_my_test_drives'))


@bp.route('/take_testdrive_<name_car>', methods=['POST', 'GET'])
@login_required
def take_test_drive(name_car):
    form = TakeTestdrive()
    price = 10
    id_car = db.session.execute(db.select(Cars.id_car).filter_by(name_car=name_car)).scalar_one()
    busy_date = db.session.query(TestDrive).filter(TestDrive.date_start > datetime.datetime.now(),
                                                   TestDrive.id_car == id_car).all()

    if request.method == 'POST':
        if form.validate_on_submit():
            date_start = form.date_start.data.strftime('%Y-%m-%d')
            date_start_date = datetime_module.strptime(date_start, '%Y-%m-%d').date()

            if date_start_date < datetime.datetime.now().date():
                flash('This date already lost', category='error')
                return redirect(url_for('.take_test_drive', name_car=name_car))
            date_end = form.date_start.data.strftime('%Y-%m-%d')

            order = db.session.execute(db.select(TestDrive).filter_by(id_car=id_car,
                                                                      date_start=date_start)).first()
            if order:
                flash('This date already busy', category='error')
                return redirect(url_for('.take_test_drive', name_car=name_car))

            test_drive = TestDrive(id_user=current_user.id_user, id_car=id_car, price=price,
                                   date_start=date_start, date_end=date_end)

            db.session.add(test_drive)
            db.session.flush()
            db.session.commit()

            subject = 'Your testdrive on: ' + name_car
            body = 'Hello, your testdrive date: ' + date_start
            car_photo = db.session.execute(db.select(Photos.name_photo).filter_by(id_car=id_car)).scalars().first()
            attachments = 'static/car_image/' + car_photo

            if CONFIG.name == 'ProductionConfig':
                send_email(subject, CONFIG.MAIL_USERNAME, [current_user.email], body, attachments)
            else:
                send_email(subject, CONFIG.MAIL_USERNAME, [current_user.email], body, attachments)
                # add_to_queue_send_email(subject, CONFIG.MAIL_USERNAME, [current_user.email], body, attachments)
                # send_test(current_user)
            flash('test_drive reserved', category='success')
            return redirect(url_for('.pay_for_test_drive'))

        else:
            flash('Error, test_drive is not reserved', category='error')
    return render_template('user/take_test_drive.html', form=form, main_menu=menu, title='Take Test drive',
                           name_car=name_car, price=price, busy_date=busy_date)


@bp.route('/pay_for_test_drive', methods=['POST', 'GET'])
@login_required
def pay_for_test_drive():
    test_drive = db.session.execute(
        db.select(TestDrive).filter_by(
            id_user=current_user.id_user).order_by(TestDrive.id_order.desc())).scalars().first()

    # если оплачивает, то данные окончательно заносятся в базу,
    # работник автосалона получает сообщение
    # на почту пользователю отправляется письмо о резерве

    return render_template('user/pay_for_test_drive.html', main_menu=menu, test_drive=test_drive)


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
                                     country=form.country.data, phone=form.phone.data)
                        db.session.add(user)
                        db.session.flush()
                        db.session.commit()
                        flash('Registration success', category='success')
                        new_user = Users.query.filter_by(email=form.email.data).first()
                        login_user(new_user)
                        flash('Welcome', category='success')

                        subject = 'You was register on testdrive'
                        body = user.name + ' Welcome!'
                        send_email(subject, CONFIG.MAIL_USERNAME, [current_user.email], body)

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


@bp.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    form = ResetPassword()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = Users.query.filter_by(email=form.email.data).first()
                if user:

                    send_password_reset_email(user)
                    flash('Check your email', category='success')
                else:
                    flash('Your email was not found', category='error')
                return redirect(url_for('.login'))
            except:
                flash('Db error', category='error')
        else:
            flash('incorrect password', category='error')

    return render_template('user/reset_password.html', main_menu=menu, title='Reset paswword', form=form)


@bp.route('/reset_password_token/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('.index'))

    user = ResetPasswordStatic.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.password.data)
        user.password = hash
        db.session.commit()
        flash('You password has been reset', category='success')
        return redirect(url_for('.login'))

    return render_template('user/reset_password.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(current_user)
        db.session.commit()


@login_manager.unauthorized_handler
def unauthorized():
    flash('Login for this action', category='error')
    return redirect(url_for('.login'))


@bp.route('/profile')
@login_required
def profile():
    profile_pic = current_user.profile_pic
    id_user = current_user.id_user
    email = current_user.email

    cached_data1 = redis.get(profile_pic)
    cached_data2 = redis.get(id_user)
    cached_data3 = redis.get(email)

    if cached_data1 and cached_data2 and cached_data3:
        image = json.loads(cached_data1)
        amount_testdrive = json.loads(cached_data2)
        amount_reviews = json.loads(cached_data3)
    else:
        amount_testdrive = db.session.query(TestDrive.id_user, db.func.count(TestDrive.id_order)).filter_by(
            id_user=id_user).group_by(TestDrive.id_user).all()[0][1]

        amount_reviews = db.session.query(
            Reviews.id_user, db.func.count(Reviews.id_review)).filter_by(
            id_user=id_user).group_by(
            Reviews.id_user).all()[0][1]

        image = current_user.profile_pic

        redis.setex(email, 20, json.dumps(str(amount_reviews)))
        redis.setex(id_user, 20, json.dumps(str(amount_testdrive)))
        redis.setex(profile_pic, 20, json.dumps(str(image)))

    if not image:
        image = url_for('static', filename='profile_image/' + 'default.jpg')
    else:
        image = url_for('static', filename='profile_image/' + image)

    return render_template('user/profile.html', main_menu=menu, title='My profile', user=current_user,
                           profile_image=image, amount_reviews=amount_reviews, amount_testdrive=amount_testdrive)


@bp.route('/profile_<alias>', methods=['GET', 'POST'])
def profile_people(alias):
    user = Users.query.filter_by(id_user=alias).first()
    if user == current_user:
        return redirect(url_for('.profile'))
    if not user.profile_pic:
        user.profile_pic = url_for('static', filename='profile_image/' + 'default.jpg')
    else:
        user.profile_pic = url_for('static', filename='profile_image/' + user.profile_pic)

    amount_testdrive = db.session.query(TestDrive.id_user, db.func.count(TestDrive.id_order)).filter_by(
        id_user=alias).group_by(TestDrive.id_user).all()
    amount_reviews = db.session.execute(
        db.select(Reviews.id_user, db.func.count(Reviews.id_review)).filter_by(id_user=alias).group_by(
            Reviews.id_user)).all()

    return render_template('user/profile_people.html', main_menu=menu, user=user, amount_reviews=amount_reviews,
                           amount_testdrive=amount_testdrive)


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
                    user.phone = form.phone.data
                    user.text = form.text.data

                    db.session.commit()
                    flash('Edit profile success', category='success')

                    return redirect(url_for('.profile'))

                except:
                    db.session.rollback()
                    flash('incorrect data or this email already use', category='error')
            else:
                flash('incorrect repeat password', category='error')
        else:
            flash('This email already use', category='error')

    return render_template('user/edit_profile.html', main_menu=menu, title='Edit_profile', form=form,
                           id_user=current_user.id_user)


@bp.route('/password_security', methods=['GET', 'POST'])
@login_required
def password_security():
    form = PasswordSecurity()

    if request.method == 'POST':

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

        return redirect(url_for('.profile'))


@bp.route('/delete_profile_<id_user>', methods=['POST'])
def delete_profile(id_user):
    if request.method == 'POST':
        try:
            profile_pic = db.session.execute(db.select(Users.profile_pic).filter_by(id_user=id_user)).scalar_one()
            if profile_pic:
                file_path = CONFIG.basepath + 'app/static/profile_image/' + profile_pic
                if os.path.exists(file_path):
                    os.remove(file_path)

            Users.query.filter_by(id_user=id_user).delete()
            db.session.commit()
            flash('profile deleted', category='success')
            return redirect(url_for('.index'))
        except:
            flash('Error, profile not deleted', category='error')

    return redirect(url_for('.profile'))


@bp.context_processor
def notifications():
    try:
        count_new_notifications = db.session.query(Messages.id_recipient, Messages.date,
                                                   db.func.count(Messages.id_message)).where(
            Messages.id_recipient == current_user.id_user,
            Messages.date > current_user.last_seen_profile).group_by(Messages.id_recipient, Messages.date).order_by(
            Messages.date.desc()).first()

        notifications = count_new_notifications[2]
    except:
        notifications = 0

    return dict(notifications=notifications)
