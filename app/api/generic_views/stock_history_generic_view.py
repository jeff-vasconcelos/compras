from django.http import JsonResponse
from rest_framework import generics

from app.models import Historico
from app.serializers.stock_history_serializer import HistoryIntegrationSerializer


class StockHistoryCreate(generics.CreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoryIntegrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Historico.objects.none()
        output_serializer = HistoryIntegrationSerializer(results, many=True)
        data = output_serializer.data[:]
        return JsonResponse({"data": data}, status=201)
