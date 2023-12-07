from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Venda
from app.serializers.sale_serializer import SaleSerializer


class SaleViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Venda.objects.all()
    serializer_class = SaleSerializer
