from django.http import JsonResponse
from rest_framework import generics

from app.models import Venda
from app.serializers.sale_serializer import SaleIntegrationSerializer


class SalesCreate(generics.CreateAPIView):
    queryset = Venda.objects.all()
    serializer_class = SaleIntegrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Venda.objects.none()
        output_serializer = SaleIntegrationSerializer(results, many=True)
        data = output_serializer.data[:]
        return JsonResponse({"data": data}, status=201)
