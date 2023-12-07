from django.http import JsonResponse
from rest_framework import generics

from app.models import Estoque
from app.serializers.stock_serializer import StockIntegrationSerializer


class StockCreate(generics.CreateAPIView):
    queryset = Estoque.objects.all()
    serializer_class = StockIntegrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Estoque.objects.none()
        output_serializer = StockIntegrationSerializer(results, many=True)
        data = output_serializer.data[:]
        return JsonResponse({"data": data}, status=201)
