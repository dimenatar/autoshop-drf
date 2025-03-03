from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User, UserRole

class BaseValidatedSerializer(serializers.Serializer):

    password = serializers.CharField()
    age = serializers.IntegerField()
    telephone = serializers.CharField()
    role = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    balance = serializers.FloatField()


    def validate_required_attr(self, data, attr_name):
        if data is None:
            raise serializers.ValidationError('Email, password, telephone and username are required')
        return data

    def validate_email(self, email):
        print(email)
        return self.validate_required_attr(email, 'email')

    def validate_password(self, password):
        return self.validate_required_attr(password, 'password')

    def validate_telephone(self, telephone):
        return self.validate_required_attr(telephone, 'telephone')

    def validate_username(self, username):
        return self.validate_required_attr(username, 'username')

    def validate_balance(self, balance):
        if balance is None:
            balance = 0
        return balance

    def validate_age(self, age):
        if age is None:
            age = 18
        return age

    def validate_role(self, role):
        if role is None:
            role = str(UserRole.Customer.name)
        return role


class RegistrationSerializer(BaseValidatedSerializer):
    password = serializers.CharField(
    )

    class Meta:
        model = User
        fields = '__all__'

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
        fields = '__all__'
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance