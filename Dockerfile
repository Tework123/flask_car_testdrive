FROM python:3.11
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY .. /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080

ENTRYPOINT FLASK_APP=/usr/src/app/flask_car_testdrive.py flask run --host=0.0.0.0

