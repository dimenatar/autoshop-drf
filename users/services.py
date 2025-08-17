from users.serializers import UserSerializer, LoginSerializer


class UserService:

    def __init__(self):
        self.user_serializer = UserSerializer
        self.serializer_class = LoginSerializer

    def get_user_data(self, request):
        serializer = self.user_serializer(request.user)

        return serializer.data
    def update_user_data(self, request):
        serializer_data = request.data.get('user', {})
        # попробуй перенести логику из UserSerializer.update прямо сюда
        serializer = self.user_serializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
        #return Response(serializer.data, status=status.HTTP_200_OK)

    def login_user(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return serializer.data


user_service = UserService()
# почитать про DI в django