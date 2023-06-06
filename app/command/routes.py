import datetime
import random
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app import db
from app.command import bp
from faker import Faker
from app.models import Users, Brands, Cars, Photos, Reviews, ReviewsPhoto

fake = Faker()


@bp.cli.command('add_user')
def add_user():
    names = ['denchik322', 'vovan', 'kama', 'mishua', 'nekit_kach', 'zavaR', 'sanya']
    emails = ['postgres@mail.ru', 'postgres1@mail.ru', 'postgres2@mail.ru', 'postgres3@mail.ru', 'postgres4@mail.ru',
              'postgres5@mail.ru', 'postgres6@mail.ru']
    password = '12345'
    country = 'russia'
    phone = '9120391209300'
    users = []
    for i in range(len(names)):
        hash = generate_password_hash(password)
        user = Users(name=names[i], password=hash, email=emails[i],
                     country=country, phone=phone)
        users.append(user)

    db.session.add_all(users)
    db.session.flush()
    db.session.commit()
    print('add_users')
    print('***Complete***')


@bp.cli.command('create_db')
@with_appcontext
def create_db():
    db.drop_all()
    db.create_all()
    print('create db')
    print('***Complete***')


@bp.cli.command('add_brands')
def add_brands():
    name_brands = ['Audi', 'BMW', 'KIA', 'Porsche', 'Ferrari']
    name_photos = ['audi-logo.png', 'bmw-logo.jpg', 'kia-logo.jpg', 'porsche-logo.jpg', 'ferrari-logo.png']
    description = [
        'Audi AG is a German automotive manufacturer of luxury vehicles headquartered in Ingolstadt, Bavaria, Germany. As a subsidiary of its parent company, the Volkswagen Group, Audi produces vehicles in nine production facilities worldwide.',

        'Bayerische Motoren Werke AG is a German multinational manufacturer of luxury vehicles and motorcycles headquartered in Munich, Bavaria, Germany. The company was founded in 1916 as a manufacturer of aircraft engines, which it produced from 1917 to 1918 and again from 1933 to 1945.',

        'Kia Corporation, commonly know formerly known as Kyungsung Precision Industry and Kia Motors Corporation), is a South Korean multinational automobile manufacturer headquartered in Seoul, South Korea. It is South Koreas second largest automobile manufacturer, after its parent company, Hyundai Motor Company, with sales of over 2.8 million vehicles in 2019.',
        'Dr. Ing. h.c. F. Porsche AG, usually shortened to Porsche  is a German automobile manufacturer specializing in high-performance sports cars, SUVs and sedans, headquartered in Stuttgart, Baden-Württemberg, Germany. The company is owned by Volkswagen AG, a controlling stake of which is owned by Porsche Automobil Holding SE.',
        'Ferrari S.p.A. is an Italian luxury sports car manufacturer based in Maranello, Italy. Founded in 1939 by Enzo Ferrari (1898–1988), the company adopted its current name in 1945 and began producing its line of cars in 1947. Ferrari became a public company in 1960, and from 1969 to 2014 it was a subsidiary of Fiat S.p.A. It was spun off from Fiat successor entity, Fiat Chrysler Automobiles, in 2016.']

    brands = []
    for i in range(len(name_brands)):
        brand = Brands(name_brand=name_brands[i], name_photo=name_photos[i])
        brands.append(brand)

    # потом посмотрим как удобно загружать сразу кучу фото на сервер через код
    # пока не понято, сначала купим хостинг.
    # file_path = CONFIG.basepath + 'app/static/brand_image/' + 123

    db.session.add_all(brands)
    db.session.flush()
    db.session.commit()
    print('add_brands')
    print('***Complete***')


@bp.cli.command('add_cars')
def add_cars():
    name_brands = ['Audi', 'BMW', 'KIA', 'Porsche', 'Ferrari']

    name_cars = [['Audi A6', 'Audi A7', 'Audi Q7'],
                 ['BMW 2', 'BMW 6', 'BMW X2'],
                 ['KIA CEED', 'KIA RIO', 'KIA Sportage'],
                 ['Porsche carrera 911', 'Porsche cayenne', 'Porsche taycan'],
                 ['f8-spider', 'f8-tributo', 'Ferrari roma']]

    description = [[
        'Price: 4 000 000, Power: 200 hp, Top Speed: 250 kmph, 0-100kmph: 6,8 seconds, Weight: 1740 kg, Price test drive: 5000',
        'Price: 5 000 000, Power: 220 hp, Top Speed: 250 kmph, 0-100kmph: 6,3 seconds, Weight: 1840 kg, Price test drive: 6000',
        'Price: 6 000 000, Power: 330 hp, Top Speed: 230 kmph, 0-100kmph: 6,1 seconds, Weight: 1960 kg, Price test drive: 7000'],
        [
            'Price: 3 000 000, Power: 140 hp, Top Speed: 220 kmph, 0-100kmph: 8,7 seconds, Weight: 1440 kg, Price test drive: 3000',
            'Price: 6 000 000, Power: 240 hp, Top Speed: 260 kmph, 0-100kmph: 6,3 seconds, Weight: 1790 kg, Price test drive: 6000',
            'Price: 3 500 000, Power: 160 hp, Top Speed: 200 kmph, 0-100kmph: 9,7 seconds, Weight: 1890 kg, Price test drive: 4000'],
        [
            'Price: 2 500 000, Power: 130 hp, Top Speed: 220 kmph, 0-100kmph: 11,0 seconds, Weight: 1740 kg, Price test drive: 2500',
            'Price: 3 000 000, Power: 130 hp, Top Speed: 220 kmph, 0-100kmph: 9,7 seconds, Weight: 1540 kg, Price test drive: 3000',
            'Price: 7 000 000, Power: 340 hp, Top Speed: 230 kmph, 0-100kmph: 7,7 seconds, Weight: 2140 kg, Price test drive: 7000'],
        [
            'Price: 10 000 000, Power: 380 hp, Top Speed: 280 kmph, 0-100kmph: 4,0 seconds, Weight: 1240 kg, Price test drive: 12000',
            'Price: 5 000 000, Power: 310 hp, Top Speed: 240 kmph, 0-100kmph: 6,7 seconds, Weight: 1950 kg, Price test drive: 6000',
            'Price: 11 000 000, Power: 400 hp, Top Speed: 300 kmph, 0-100kmph: 5,0 seconds, Weight: 1440 kg, Price test drive: 13000'],
        [
            'Price: 21 000 000, Power: 720 hp, Top Speed: 330 kmph, 0-100kmph: 2,9 seconds, Weight: 1260 kg, Price test drive: 20000',
            'Price: 18 000 000, Power: 700 hp, Top Speed: 320 kmph, 0-100kmph: 3,0 seconds, Weight: 1340 kg, Price test drive: 18000',
            'Price: 17 000 000, Power: 620 hp, Top Speed: 320 kmph, 0-100kmph: 3,4 seconds, Weight: 1420 kg, Price test drive: 17000']]

    name_photos = [
        [['audi_A6-1.jpg', 'audi_A6-2.jpg', 'audi_A6-3.jpg'],
         ['audi_A7-1.jpg', 'audi_A7-2.jpg', 'audi_A7-3.jpg'],
         ['audi_Q7-1.jpg', 'audi_Q7-2.jpg', 'audi_Q7-3.jpg']],
        [['BMW_2-1.jpg', 'BMW_2-2.jpg', 'BMW_2-3.jpg'],
         ['BMW_6-1.jpg', 'BMW_6-2.jpg', 'BMW_6-3.jpg'],
         ['BMW_X2-1.jpg', 'BMW_X2-2.jpg', 'BMW_X2-3.jpg']],
        [['KIA_CEED-1.jpg', 'KIA_CEED-2.jpg', 'KIA_CEED-3.jpg'],
         ['KIA_RIO-1.jpg', 'KIA_RIO-2.jpg', 'KIA_RIO-3.jpg'],
         ['KIA_Sportage-1.jpg', 'KIA_Sportage-2.jpg', 'KIA_Sportage-3.jpg']],
        [['porshe_carrera_911-1.jpg', 'porshe_carrera_911-2.jpg', 'porshe_carrera_911-3.jpg'],
         ['porshe_cayenne-1.jpg', 'porshe_cayenne-2.jpg', 'porshe_cayenne-3.jpg'],
         ['porshe_taycan-1.jpg', 'porshe_taycan-2.jpg', 'porshe_taycan-3.jpg']],
        [['f8-spider-1.jpg', 'f8-spider-2.jpg', 'f8-spider-3.jpg'],
         ['f8-tributo-1.jpg', 'f8-tributo-2.jpg', 'f8-tributo-3.jpg'],
         ['ferrari_roma-1.jpg', 'ferrari_roma-2.jpg', 'ferrari_roma-3.jpg']]]

    url_videos = [[
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/4K4Is06NRfk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/VpNX324owaQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/PWwOCAEusow" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'],
        [
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/huWiIGzcEIc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/E60tFfljUnY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/WlVY2p4nQAg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'],
        [
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/vOEkzQFMkHs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/q9ebDiC2DkI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/0Ghjlt1GvSg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'],
        [
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/yIv9-AEIpZc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/X24wzcFGK68" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/qinXZ7qwAMI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'],
        [
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/MWU1-5YInPs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/qGoVT3LVKAU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/nh6czgbRgtc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>']]

    for i in range(len(name_brands)):
        id_brand = db.session.execute(db.select(Brands.id_brand).filter_by(name_brand=name_brands[i])).scalar_one()
        count = 0
        for j in range(3):
            car = Cars(name_car=name_cars[i][j], description=description[i][j],
                       id_brand=id_brand, url_video=url_videos[i][j])

            db.session.add(car)
            db.session.flush()
            db.session.commit()

            id_car = db.session.execute(db.select(Cars.id_car).filter_by(name_car=name_cars[i][j])).scalar_one()
            whole_photo = []
            for k in range(3):
                name_photo_db = Photos(id_car=id_car, name_photo=name_photos[i][j][k])
                whole_photo.append(name_photo_db)

                # file_path = CONFIG.basepath + 'app/static/car_image/' + 123

            db.session.add_all(whole_photo)
            db.session.flush()
            db.session.commit()
            count += 1
            print(f'add {name_cars[i][j]}, {count}')
    print('add_cars')
    print('***Complete***')


@bp.cli.command('add_reviews')
def add_reviews():
    name_cars = ['Audi A6', 'Audi A7', 'Audi Q7',
                 'BMW 2', 'BMW 6', 'BMW X2',
                 'KIA CEED', 'KIA RIO', 'KIA Sportage',
                 'Porsche carrera 911', 'Porsche cayenne', 'Porsche taycan',
                 'f8-spider', 'f8-tributo', 'Ferrari roma']

    for i in range(len(name_cars)):

        id_car = db.session.execute(db.select(Cars.id_car).filter_by(name_car=name_cars[i])).scalar_one()

        emails = ['postgres@mail.ru', 'postgres1@mail.ru', 'postgres2@mail.ru', 'postgres3@mail.ru',
                  'postgres4@mail.ru',
                  'postgres5@mail.ru', 'postgres6@mail.ru']

        degree = [1, 2, 3, 4, 5]
        photo = True
        for j in range(len(emails)):
            id_user = db.session.execute(db.select(Users.id_user).filter_by(email=emails[j])).scalar_one()
            review = Reviews(id_car=id_car, id_user=id_user, text=fake.text(), degree=random.choice(degree),
                             date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(review)
            db.session.flush()
            db.session.commit()

            if photo:
                id_review = db.session.execute(
                    db.select(Reviews.id_review).filter_by(id_car=id_car, id_user=id_user)).scalar_one()

                name_photo_db = ReviewsPhoto(id_review=id_review)
                db.session.add(name_photo_db)
                db.session.flush()
                db.session.commit()
                # photo_id = db.session.execute(
                #     db.select(ReviewsPhoto.id_photo).filter_by(id_review=id_review)).scalars().first()
                #
                # file_path = CONFIG.basepath + 'app/static/reviews_photo/' + str(photo_id) + '.jpg'

    print('add_reviews')
    print('***Complete***')
