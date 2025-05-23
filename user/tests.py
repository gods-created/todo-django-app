from django.test import TestCase
from faker import Faker
from .models import User

class Tests(TestCase):
    @classmethod
    def setUpClass(cls):
        faker = Faker()
        cls.user_data = {
            'username': faker.user_name(),
            'email': faker.email(),
            'password': faker.password()
        }

        cls.user = None

    def test_1_create_user(self):
        user_data = Tests.user_data
        user = Tests.user = User.objects.create_user(**user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, user_data['username'])

    def test_2_auth_request(self):
        request = self.client.post(
            path='/user/auth/',
            headers={},
            data=Tests.user_data
        )

        status = request.status_code
        response = request.json()

        self.assertEqual(status, 200)
        self.assertIn('access_token', response)

    @classmethod
    def tearDownClass(cls):
        if cls.user:
            _, *_ = User.objects.filter(username=cls.user_data['username']).delete()
