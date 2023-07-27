import base64
import os

import requests as requests


class BearerAuth:
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['authorization'] = 'Bearer ' + self.token
        return r


token = 'KU32jaODN8FQSxNGL4W7bKZzNY+pPgbQ'

r = requests.get('http://127.0.0.1:5000/api/get_image_cars',
                 auth=BearerAuth('KU32jaODN8FQSxNGL4W7bKZzNY+pPgbQ'))

images = r.json()['data']

count = 0
for i in range(len(images)):
    imgdata = base64.b64decode(images[i])
    filename = str(i) + '.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)
    count += 1
print(count)
count = 45
if count == 45:
    for j in range(count):
        file = str(j) + '.jpg'
        os.remove(file)
print('ok')
