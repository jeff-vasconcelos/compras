from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Fornecedor
from app.serializers.provider_serializer import ProviderSerializer


class ProviderViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Fornecedor.objects.all()
    serializer_class = ProviderSerializer
