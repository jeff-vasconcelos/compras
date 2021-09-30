from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.serializer_integration import *
from core.models.empresas_models import Filial


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def access_valid(request):

    return Response("API - Insight")


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def listar_produtos_empresa(request, pk):
    qs = Produto.objects.filter(empresa_id__exact=pk).order_by('-id')
    serializer = ProdSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def listar_fornecedor_empresa(request, pk):
    qs = Fornecedor.objects.filter(empresa_id__exact=pk).order_by('-id')
    serializer = FornecSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def listar_filiais_empresa(request, pk):
    qs = Filial.objects.filter(empresa_id__exact=pk).order_by('-id')
    serializer = FilialSerializer(qs, many=True)
    return Response(serializer.data)


class FornecedorCreate(generics.CreateAPIView):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Fornecedor.objects.none()
        output_serializer = FornecSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)


class ProdutoCreate(generics.CreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Produto.objects.none()
        output_serializer = ProdSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)


class HistoricoCreate(generics.CreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Historico.objects.none()
        output_serializer = HistSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)


class VendaCreate(generics.CreateAPIView):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Venda.objects.none()
        output_serializer = VendaSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)


class PedidoCreate(generics.CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Pedido.objects.none()
        output_serializer = PedSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)


class EntradaCreate(generics.CreateAPIView):
    queryset = Entrada.objects.all()
    serializer_class = EntSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Entrada.objects.none()
        output_serializer = EntSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)


class EstoqueCreate(generics.CreateAPIView):
    queryset = Estoque.objects.all()
    serializer_class = EstSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Estoque.objects.none()
        output_serializer = EstSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)
