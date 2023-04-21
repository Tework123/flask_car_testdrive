from app import app, login_manager
from flask import Flask, render_template, request

from app.models import Users, MainMenu
from app import db

menu = [['Home', '/'], ['Сar brands', '/user/car_brands'], ['Sing in', '/user/login'],
        ['Registration', '/user/register']]


@app.route('/')
def index():
    return render_template('index.html', title='Home', main_menu=menu)


if __name__ == '__main__':
    with app.app_context():
        # импорт и регистрация blueprint
        from app.user import bp as bp_user

        app.register_blueprint(bp_user, url_prefix='/user')

        from app.admin import bp as bp_admin

        app.register_blueprint(bp_admin, url_prefix='/admin')
        # db.drop_all()
        # db.create_all()

        # a = Users.query.all()
        # print(a)
        # for i in a:
        #     print(i.email)

        # me = Users(name='chren', email='adddd@mail', country='russia', password='23123pass')
        # db.session.add(me)
        # db.session.commit()

        # menu = [['Home', '/'], ['Сar brands', '/user/car_brands'], ['Sing in', '/user/login'], ['Registration', '/user/register']]
        # for i in menu:
        #     head = MainMenu(text=i[0], url=i[1])
        #     db.session.add(head)
        #
        # db.session.commit()
        # a = Users.query.all()
        # res = db.session.query(Users, Profiles).join( Profiles, Users.id == Profiles.user_id).all()
        # print(a)
        # print(res)
        #     db.create_all()

        # Создание базы данных
    # from main import db
    #
    # db.create_all()
    app.run(debug=True)
