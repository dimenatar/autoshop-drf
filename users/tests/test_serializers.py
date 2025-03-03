from rest_framework import serializers
from rest_framework.test import APITestCase

from users.models import User, UserRole
from users.serializers import LoginSerializer, UserSerializer, RegistrationSerializer


class UsersSerializersTestCase(APITestCase):
    def testLogin(self):
        expected_data, serialized_data = self.getTestDatas(LoginSerializer)

        assert sorted(expected_data) == sorted(serialized_data)

    def testUpdateUserData(self):
        expected_data, serialized_data = self.getTestDatas(UserSerializer)

        assert sorted(expected_data) == sorted(serialized_data)

    def getTestDatas(self, serializer):
        serialized_data = self.getSerializedData(serializer)
        expected_data = self.getTestData(serialized_data['password'])
        return expected_data, serialized_data

    def getSerializedData(self, serializer):
        user1 = User.objects.create_user(username='test', email='email', telephone='++', age=11, balance=0, password='pass')
        serialized_data = serializer(user1).data
        return serialized_data

    def testRegistration(self):
        expected_data, serialized_data = self.getTestDatas(RegistrationSerializer)
        assert sorted(expected_data) == sorted(serialized_data)
        pass


    def getTestData(self, password):
        return {
                'username':'test',
                'email':'email',
                'telephone':'++',
                'age':'11',
                'balance': 0.0,
                'password':password,
                'role':str(UserRole.Customer),
        }