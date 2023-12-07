from django.http import JsonResponse
from rest_framework import generics

from app.models import Produto
from app.serializers.product_serializer import ProductIntegrationSerializer


class ProductCreate(generics.CreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProductIntegrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Produto.objects.none()
        output_serializer = ProductIntegrationSerializer(results, many=True)
        data = output_serializer.data[:]
        return JsonResponse({"data": data}, status=201)
