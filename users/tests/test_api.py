import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

client = APIClient()
BASE_URL = 'http://localhost:8000'

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass

@pytest.fixture()
def get_test_user():
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

def test_registration(get_test_user):
    url = BASE_URL + '/api/users/'

    test_user = dict(get_test_user)

    response = client.post(url, {"user": test_user["user"]["username"]}, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response: Response = client.post(url, get_test_user, format='json')

    assert response.status_code == status.HTTP_201_CREATED


def test_login(get_test_user):
    url_register = BASE_URL + '/api/users/'
    url_login = BASE_URL + '/api/users/login/'

    response_login = client.post(url_login, get_test_user, format='json')

    assert response_login.status_code == status.HTTP_400_BAD_REQUEST
    response: Response = client.post(url_register, get_test_user, format='json')
    response_login = client.post(url_login, get_test_user, format='json')

    assert response_login.status_code == status.HTTP_200_OK


def test_update_user(get_test_user):
    url_register = BASE_URL + '/api/users/'
    url_token = BASE_URL + '/api/token/'

    response: Response = client.post(url_register, get_test_user, format='json')
    token_response: Response = client.post(url_token, {"password": get_test_user["user"].get("password"),
                                                       "email": get_test_user["user"].get("email")}, format='json')
    access_token = 'Bearer ' + str(token_response.data['access'])

    url = BASE_URL + '/api/user/'

    get_test_user['user']['password'] = 'updated_password'
    get_test_user['user']['telephone'] = 'mmmmmmmmmm'

    token_headers = {'Authorization': access_token}
    response = client.put(path=url, data=get_test_user, headers=token_headers, format='json')

    assert response.status_code == status.HTTP_200_OK
