import os
from wsgiref.simple_server import WSGIRequestHandler

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from tests.confest import *

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass

client = APIClient()
BASE_URL = os.environ.get('BASE_URL')

class TestAuth:
    def test_registration(self, get_test_user):
        url = BASE_URL + '/api/auth/users/'
        test_user = dict(get_test_user)
        response = client.post(url, {"user": test_user["user"]["username"]}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response: Response = client.post(url, get_test_user, format='json')
        assert response.status_code == status.HTTP_201_CREATED


    def test_login(self, get_test_user):
        url_login = BASE_URL + '/api/auth/users/login/'
        url_register = BASE_URL + '/api/auth/users/'
        response: Response = client.post(url_register, get_test_user, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        response_login = client.post(url_login, get_test_user, format='json')

        assert response_login.status_code == status.HTTP_200_OK


class TestUser:
    def test_update_user(self, get_test_user):

        url_register = BASE_URL + '/api/auth/users/'
        response: Response = client.post(url_register, get_test_user, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        url_token = BASE_URL + '/api/token/'

        token_response: Response = client.post(url_token, {"password": get_test_user["user"].get("password"),
                                                           "email": get_test_user["user"].get("email")}, format='json')
        print(f'dataaaaaaaaa {token_response.data}')
        access_token = 'Bearer ' + str(token_response.data['access'])

        url = BASE_URL + '/api/auth/user/'

        get_test_user['user']['password'] = 'updated_password'
        get_test_user['user']['telephone'] = 'mmmmmmmmmm'

        token_headers = {'Authorization': access_token}
        response = client.put(path=url, data=get_test_user, headers=token_headers, format='json')

        assert response.status_code == status.HTTP_200_OK
