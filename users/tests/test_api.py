from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

class UsersApiTestCase(APITestCase):

    BASE_URL = 'http://localhost:8000'

    def test_registration(self):

        url = UsersApiTestCase.BASE_URL + '/api/users/'

        test_user = self.getTestUser()
        test_user['user'].pop('email')
        test_user['user'].pop('username')

        response = self.client.post(url, test_user, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response:Response = self.client.post(url, self.getTestUser(), format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def getTestUser(self):
        return {
            "user":
                {
                    "username": "test_user",
                    "email": "test_email@sobaka.ru",
                    "telephone": "telephone",
                    "age": 11,
                    "balance": "0",
                    "role": "Customer",
                    "password": "test_password",
                }
        }

    def test_login(self):
        url_register = UsersApiTestCase.BASE_URL + '/api/users/'
        url_login = UsersApiTestCase.BASE_URL + '/api/users/login/'

        user = self.getTestUser()

        response_login = self.client.post(url_login, user, format='json')

        assert response_login.status_code == status.HTTP_400_BAD_REQUEST
        response: Response = self.client.post(url_register, self.getTestUser(), format='json')
        response_login = self.client.post(url_login, user, format='json')

        assert response_login.status_code == status.HTTP_200_OK

    def test_update_user(self):

        user = self.getTestUser()
        url_register = UsersApiTestCase.BASE_URL + '/api/users/'
        url_token = 'https://localhost:8000/api/token/'

        response: Response = self.client.post(url_register, self.getTestUser(), format='json')
        token_response: Response = self.client.post(url_token, {"password":user["user"].get("password"), "email":user["user"].get("email")}, format='json')
        access_token = 'Bearer ' + str(token_response.data['access'])

        url =  UsersApiTestCase.BASE_URL + '/api/user/'

        user['user']['password'] = 'updated_password'
        user['user']['telephone'] = 'mmmmmmmmmm'

        token_headers = {'Authorization': access_token}
        response = self.client.put(path=url, data=user, headers=token_headers, format='json')

        assert response.status_code == status.HTTP_200_OK