from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User, UserRole

class BaseValidatedSerializer(serializers.Serializer):

    password = serializers.CharField(
        #ax_length=128,
        #min_length=8,
        #write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    age = serializers.IntegerField()
    telephone = serializers.CharField()
    role = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField()
    balance = serializers.FloatField()

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        name = data.get('name', None)
        age = data.get('age', None)
        telephone = data.get('telephone', None)
        role = data.get('role', None)
        balance = data.get('balance', None)
        token = data.get('token', None)

        if (email is None ) or (password is None) or (name is None) or (telephone is None):
            raise serializers.ValidationError('Email, password, telephone and name are required')

        if role is None:
            role = str(UserRole.Customer.name)
        if balance is None:
            balance = 0.0
        if age is None:
            age = 18


        return {
            'email': email,
            'name': name,
            #'token': token,
            'age': age,
            'password': password,
            'telephone': telephone,
            'balance': balance,
            'role': role,
        }


class RegistrationSerializer(BaseValidatedSerializer):
    password = serializers.CharField(
        #max_length=128,
        #min_length=8,
        #write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'age', 'telephone', 'token', 'password', 'role', 'balance',]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(BaseValidatedSerializer):


    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )


        return super().validate(data)

class UserSerializer(BaseValidatedSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'age', 'telephone', 'password', 'role', 'balance',)
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance