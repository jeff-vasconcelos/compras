from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Estoque
from app.serializers.stock_serializer import StockSerializer


class CurrentStockViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Estoque.objects.all()
    serializer_class = StockSerializer
