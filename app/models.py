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

    # def create(self, user):
    #     self.__user = user
    #     return self

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


class Orders(db.Model):
    id_order = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    id_car = db.Column(db.Integer, db.ForeignKey('cars.id_car'))
    date_start = db.Column(db.DateTime, default=datetime.now())
    date_end = db.Column(db.DateTime, default=datetime.now())


class Cars(db.Model):
    id_car = db.Column(db.Integer, primary_key=True)
    id_brand = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    id_photos = db.Column(db.Integer)
    id_video = db.Column(db.Integer)

    # def __repr__(self):
    #     return f'<users {self.id}>'

# class Profiles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=True)
#     city = db.Column(db.String(100))
#
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
