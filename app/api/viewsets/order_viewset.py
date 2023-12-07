from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Pedido
from app.serializers.order_serializer import OrderSerializer


class OrderViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Pedido.objects.all()
    serializer_class = OrderSerializer
