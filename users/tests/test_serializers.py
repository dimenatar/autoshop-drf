from rest_framework.test import APITestCase

from users.models import User, UserRole
from users.serializers import LoginSerializer


class UsersSerializersTestCase(APITestCase):
    def testLogin(self):
        expectedData, serializedData = self.getTestDatas()

        self.assertEqual(sorted(serializedData), sorted(expectedData))

    def testUpdateUserData(self):
        expectedData, serializedData = self.getTestDatas()

        self.assertEqual(sorted(serializedData), sorted(expectedData))

    def getTestDatas(self):
        serializedData = self.getSerializedData()
        expectedData = self.getTestData(serializedData['token'], serializedData['password'])
        return expectedData, serializedData

    def getSerializedData(self):
        user1 = User.objects.create_user(name='test', email='email', telephone='++', age=11, balance=0, password='pass')
        serializedData = LoginSerializer(user1).data
        return serializedData

    def testRegistration(self):
        expectedData, serializedData = self.getTestDatas()
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