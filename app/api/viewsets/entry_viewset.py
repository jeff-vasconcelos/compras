from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Entrada
from app.serializers.entry_serializer import EntrySerializer


class EntryViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Entrada.objects.all()
    serializer_class = EntrySerializer
