from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Historico
from app.serializers.stock_history_serializer import HistorySerializer


class StockHistoryViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Historico.objects.all()
    serializer_class = HistorySerializer
