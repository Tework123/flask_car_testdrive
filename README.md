Flask_car_testdrive

Сайт для заказа автомобилей на тест-драйв

Ссылка на сайт:
https://tework123.ru/

Ссылка на гитхаб:
https://github.com/Tework123/flask_car_testdrive/

Использованные технологии:
- Flask
Веб-фреймворк
- Flask-login
Создает сессии и куки
- Flask-SQLAlchemy
Позволяет работать с базой данных через python классы и функции
- Flask-migrate
Обеспечивает миграции базы данных
- Flask-Mail
Отправляет сообщения на почту
- Pytest
unit test
- WTForms
Проверка введенных данных в поля
- Jinja2
Позволят создавать html шаблоны
- PyJWT
Создает jwt токен для использования api


Веб-приложение развернуто на VPS с помощью docker.
Docker-conteiners: 
- nginx 
- flask(gunicorn)
- db(postgres)
- pgbackups
- certbot
- redis(cash)

Стартовая страница сайта:
![Снимок экрана от 2023-07-27 06-49-10](https://github.com/Tework123/flask_car_testdrive/assets/115368408/41092a64-75d8-4f61-93e9-a3c7ba5b6d0e)


Схема базы данных:
![image](https://github.com/Tework123/flask_car_testdrive/assets/115368408/6c15c61f-46a7-472a-88e3-482a0f171769)

Реализованная функциональность сайта:
- регистрация пользователей
- восстановление пароля по почте
- панель админа для добавления контента
- заказ автомобиля
- отправка сообщений
- api для получение контента

Also:
- unit test api
- кеширование стартовой страницы

Установка:

Создаем новую папку, создаем виртуальное окружение, активируем его.

Подключаем git к папке:

    git init 
    git clone https://github.com/Tework123/flask_car_testdrive.git
    
Заходим в папку с приложением flask:

    cd flask_car_testdrive
    cd flask_car_testdrive
    
Устанавливаем зависимости:

    pip install -r requirements.txt

Создаем два .env файла, один в папке с приложением flask, другой в папке с docker-compose.

Заполняем .env файл примерно так:

    SQLALCHEMY_DATABASE_URI_POSTGRES = 'postgresql://postgres:password@localhost:5432/name_db'
    SQLALCHEMY_DATABASE_URI_POSTGRES_prod = 'postgresql://postgres:password@db:5432/name_db'
    SQLALCHEMY_DATABASE_URI_POSTGRES_TEST = 'postgresql://postgres:password@localhost:5432/name_db_test'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'password'
    POSTGRES_DB = 'name_db'

    SECRET_KEY = 'asldkk12kelakfjafkj23jijraijfi23jappweovm1'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'myemail@gmail.com'
    MAIL_PASSWORD = 'sadasdkmvxvvqlwl'
    ADMINS = 'myemail@gmail.com'
    ADMIN_LOGIN = 'admin@admin.com'
    ADMIN_PASSWORD = 'admin'
    REDIS_URL_LOCAL = 'redis://127.0.0.1:6379'
    REDIS_URL_server = 'redis://redis:6379'
    REDIS_PASSWORD = 'mzxcvm213zmvdsf@k3ll1'

Локально поднимаем postgres, redis
