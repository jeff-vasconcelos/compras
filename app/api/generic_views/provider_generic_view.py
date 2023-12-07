from django.http import JsonResponse
from rest_framework import generics

from app.models import Fornecedor
from app.serializers.provider_serializer import ProviderIntegrationSerializer


class ProvidersCreate(generics.CreateAPIView):
    queryset = Fornecedor.objects.all()
    serializer_class = ProviderIntegrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Fornecedor.objects.none()
        output_serializer = ProviderIntegrationSerializer(results, many=True)
        data = output_serializer.data[:]
        return JsonResponse({"data": data}, status=201)
