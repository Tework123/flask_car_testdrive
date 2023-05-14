from main import app


# @pytest.fixture()
# def test_index():
#     response = app.test_client().get('/user/')
#     assert response.status_code == 200

# @pytest.mark.usefixtures('db')
# class TestBasic():
#     def test_home(self, client):
#         res = client.get('/')
#         assert res.status_code == 200

class TestViews:

    def setup(self):
        print('hello')
        # create_app(app)
        app.testing = True
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_user(self):
        response = self.client.get('/user/')
        assert response.status_code == 200

    def teardown(self):
        print('end)')
