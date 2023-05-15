from app.models import Users, Cars


# registration
def test_users():
    user = Users(email='avottak@gmail.com',
                 name='tework',
                 country='usa',
                 password='123456',
                 phone='2919299219',
                 text='hello123'
                 )
    assert user.email == 'avottak@gmail.com'
    assert user.name == 'tework'
    assert user.country == 'usa'
    assert user.password == '123456'
    assert user.phone == '2919299219'
    assert user.text == 'hello123'


def test_cars():
    car = Cars(name_car='ferrari',
               description='lololololo',
               url_video=range(999))
    assert car.name_car == 'ferrari'
    assert car.description == 'lololololo'
    assert len(car.url_video) < len(range(1000))
