from rest_framework import serializers
from rest_framework.test import APITestCase

from users.models import User, UserRole
from users.serializers import LoginSerializer, UserSerializer, RegistrationSerializer


class UsersSerializersTestCase(APITestCase):
    def testLogin(self):
        expectedData, serializedData = self.getTestDatas(LoginSerializer)

        self.assertEqual(sorted(serializedData), sorted(expectedData))

    def testUpdateUserData(self):
        expectedData, serializedData = self.getTestDatas(UserSerializer)

        self.assertEqual(sorted(serializedData), sorted(expectedData))

    def getTestDatas(self, serializer):
        serializedData = self.getSerializedData(serializer)
        expectedData = self.getTestData(serializedData['token'], serializedData['password'])
        return expectedData, serializedData

    def getSerializedData(self, serializer):
        user1 = User.objects.create_user(username='test', email='email', telephone='++', age=11, balance=0, password='pass')
        serializedData = serializer(user1).data
        return serializedData

    def testRegistration(self):
        expectedData, serializedData = self.getTestDatas(RegistrationSerializer)
        self.assertEqual(sorted(serializedData), sorted(expectedData))
        pass


    def getTestData(self, token, password):
        return {
                'token': token,
                'name':'test',
                'email':'email',
                'telephone':'++',
                'age':'11',
                'balance': 0.0,
                'password':password,
                'role':str(UserRole.Customer),

        }