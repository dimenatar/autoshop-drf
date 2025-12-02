from core.views import BaseListView, BaseSingleItemView
from users.models import User
from users.serializers import UserSerializer


class UserListView(BaseListView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(BaseSingleItemView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
