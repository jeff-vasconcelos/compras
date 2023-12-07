from django.http import JsonResponse
from rest_framework import generics

from app.models import Pedido
from app.serializers.order_serializer import OrderIntegrationSerializer


class OrdersCreate(generics.CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = OrderIntegrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Pedido.objects.none()
        output_serializer = OrderIntegrationSerializer(results, many=True)
        data = output_serializer.data[:]
        return JsonResponse({"data": data}, status=201)
