from app import app, login_manager
from flask import Flask, render_template, request

from app.models import Users, MainMenu
from app import db

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return Users.get(user_id)


@app.route('/')
def index():
    main_menu = MainMenu.query.all()
    return render_template('index.html', title='Home', main_menu=main_menu)


if __name__ == '__main__':
    with app.app_context():
        # импорт и регистрация blueprint
        from app.user import bp as bp_user

        app.register_blueprint(bp_user)

        from app.admin import bp as bp_admin

        app.register_blueprint(bp_admin)
        # db.drop_all()
        # db.create_all()

        # a = Users.query.all()
        # print(a)
        # for i in a:
        #     print(i.email)

        # me = Users(name='chren', email='adddd@mail', country='russia', password='23123pass')
        # db.session.add(me)
        # db.session.commit()

        menu = [['Home', '/'], ['Сar brands', '/car_brands'], ['Sing in', '/login'], ['Registration', '/register']]
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
    #  from main import db
    # db.create_all()
    app.run(debug=True)
