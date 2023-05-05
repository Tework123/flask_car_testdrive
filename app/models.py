from app import db, login_manager
from datetime import datetime


class MainMenu(db.Model):
    head_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(30), unique=True)
    url = db.Column(db.String(30), unique=True)


class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), unique=True)
    country = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(500), nullable=True)
    profile_pic = db.Column(db.String(), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id_user)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


# change this
class Cars(db.Model):
    id_car = db.Column(db.Integer, primary_key=True)
    name_car = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(2000))
    id_brand = db.Column(db.Integer, db.ForeignKey('brands.id_brand', ondelete='CASCADE'))


class Photos(db.Model):
    id_photo = db.Column(db.Integer, primary_key=True)
    id_car = db.Column(db.Integer, db.ForeignKey('cars.id_car', ondelete='CASCADE'))
    name_photo = db.Column(db.String, unique=True)


class Brands(db.Model):
    id_brand = db.Column(db.Integer, primary_key=True)
    name_brand = db.Column(db.String, unique=True)
    name_photo = db.Column(db.String, unique=True)
    description = db.Column(db.String)


class Videos(db.Model):
    id_video = db.Column(db.Integer, primary_key=True)
    id_car = db.Column(db.Integer, db.ForeignKey('cars.id_car', ondelete='CASCADE'))
    url = db.Column(db.String, unique=True)


class Reviews(db.Model):
    id_review = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_car = db.Column(db.Integer, db.ForeignKey('cars.id_car'))
    date = db.Column(db.DateTime)
    text = db.Column(db.String(5000))
    degree = db.Column(db.Integer)


class ReviewsPhoto(db.Model):
    id_review = db.Column(db.Integer, db.ForeignKey('reviews.id_review', ondelete='CASCADE'))
    id_photo = db.Column(db.Integer, primary_key=True)
#
#
# class Orders(db.Model):
#     id_order = db.Column(db.Integer, primary_key=True)
#     price = db.Column(db.Integer)
#     id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
#     id_car = db.Column(db.Integer, db.ForeignKey('cars.id_car'))
#     date_start = db.Column(db.DateTime, default=datetime.now())
#     date_end = db.Column(db.DateTime, default=datetime.now())
