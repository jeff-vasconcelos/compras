from django.http import JsonResponse
from rest_framework import generics

from app.models import Entrada
from app.serializers.entry_serializer import EntryIntegrationSerializer


class EntryCreate(generics.CreateAPIView):
    queryset = Entrada.objects.all()
    serializer_class = EntryIntegrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Entrada.objects.none()
        output_serializer = EntryIntegrationSerializer(results, many=True)
        data = output_serializer.data[:]
        return JsonResponse({"data": data}, status=201)
