FROM python:3.11
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY .. /usr/src/app/

RUN pip install --no-cache-dir --upgrade pip  && pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "flask_car_testdrive:app"]


# сделать последний версии модулей, но не latest, захостить на сервак, проверить работу redis, gunicorn, nginx,
# запускать с помощью докер.прод, а то оперативки не хватает