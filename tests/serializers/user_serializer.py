import pytest

from users.models import User
from users.serializers import LoginSerializer, UserSerializer, RegistrationSerializer
from users.user_manager import UserRole

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass

def testLogin():
    expected_data, serialized_data = getTestDatas(LoginSerializer)

    assert sorted(expected_data) == sorted(serialized_data)


def testUpdateUserData():
    expected_data, serialized_data = getTestDatas(UserSerializer)

    assert sorted(expected_data) == sorted(serialized_data)


def getTestDatas(serializer):
    serialized_data = getSerializedData(serializer)
    expected_data = getTestData(serialized_data['password'])
    return expected_data, serialized_data


def getSerializedData(serializer):
    user1 = User.objects.create_user(username='test', email='email', telephone='++', age=11, balance=0, password='pass')
    serialized_data = serializer(user1).data
    return serialized_data


def testRegistration():
    expected_data, serialized_data = getTestDatas(RegistrationSerializer)
    assert sorted(expected_data) == sorted(serialized_data)


def getTestData(password):
    return {
        'username': 'test',
        'email': 'email',
        'telephone': '++',
        'age': '11',
        'balance': 0.0,
        'password': password,
        'role': str(UserRole.Customer),
    }
