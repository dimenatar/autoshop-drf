from cars.models import Car
from cars.serializers import CarSerializer
from core.views import BaseListView, BaseSingleItemView


class CarListView(BaseListView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarView(BaseSingleItemView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
