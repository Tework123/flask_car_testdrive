import time
from datetime import date

import jwt

config = {
    "version": "3.0",
    "type": "rest_api",
    "private_key_id": "6093d8ce-0e03-4ac3-ad50-31819c4fdd71",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQghOViV3OWZhdwTp35\n7WPIQw2rIJ5+YkmRUuu8/4rbd76hRANCAARKBPJ9//fD91i9Rmv4hbZDuuKLwmfM\nekVRfNuIQ2L+bM2Ztew7TvdjeOlDe3ZLdj2NzG2qJek60QBYUmqBmifJ\n-----END PRIVATE KEY-----\n\n",
    "app_uri": "https://sandbox.rest-api.high-mobility.com/v5",
    "app_id": "5082380C6E8A50198176C067",

    "client_serial_number": "1F1121AE7AD6BF474B",
    'jti': '123fsfjji34tsjfls'

}

json_data = {
    'ver': config['version'],
    'aud': config['app_uri'],
    'iss': config['client_serial_number'],
    'iat': time.time_ns(),
    'jti': config['jti'],
    'sub': 123

}

SECRET_KEY = 'adskgjskdjg234fFJKASkk1234349itagjkjLKSA'


def create_jwt():
    encode_data = jwt.encode(payload=json_data, key=SECRET_KEY, algorithm='HS256')
    print(encode_data)
    # print(time.time_ns())


create_jwt()
