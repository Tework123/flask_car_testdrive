Flask_car_testdrive

Ссылка на сайт:
https://tework123.ru/

Ссылка на гитхаб:
https://github.com/Tework123/flask_car_testdrive/

Использованные технологии:
- Веб-фреймворк: flask
Библиотеки:
- Flask-login
Создает сессии и куки
- Flask-SQLAlchemy
Позволяет работать с базой данных через python классы и функции
- Flask-migrate
Обеспечивает миграции базы данных
- Flask-Mail
Отправляет сообщения на почту
- pytest
unit test
- WTForms
Проверка введенных данных в поля
- Jinja2
Позволят создавать html шаблоны
- PyJWT
Создает jwt токен для использования api


Веб-приложение запущено на VPS с помощью docker.
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
