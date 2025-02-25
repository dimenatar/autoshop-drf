from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from users.models import UserRole

class UsersApiTestCase(APITestCase):
    def test_registration(self):

        url = 'http://127.0.0.1:8000/api/users/'

        test_user = self.getTestUser()
        test_user['user'].pop('email')
        test_user['user'].pop('name')

        response = self.client.post(url, test_user, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response:Response = self.client.post(url, self.getTestUser(), format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def getTestUser(self):
        return {
            "user": {
                "name": "name",
                "email": "customemail@sobaka.sutulaya",
                "password": "<PASSWORD>",
                "telephone": "12345678",
                "age": 11,
                "balance": 1000,
                "role": str(UserRole.Customer.name),
                "is_active": True,
            }
        }

    def test_login(self):
        url_register = 'http://127.0.0.1:8000/api/users/'
        url_login = 'http://127.0.0.1:8000/api/users/login/'
        user = self.getTestUser()

        response_login = self.client.post(url_login, user, format='json')

        self.assertEqual(response_login.status_code, status.HTTP_400_BAD_REQUEST)

        response: Response = self.client.post(url_register, self.getTestUser(), format='json')
        response_login = self.client.post(url_login, user, format='json')

        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        url = 'http://127.0.0.1:8000/api/user'
        user = self.getTestUser()
        user['user']['password'] = 'updated_password'
        user['user']['telephone'] = 'mmmmmmmmmm'

        print('test update user:', user)

        response = self.client.put(url, user, format='json')

        print(response, response.data)


        self.assertEqual(response.status_code, status.HTTP_200_OK)