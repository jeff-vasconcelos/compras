from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.serializer import *
from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque import Estoque
from api.models.historico import Historico
from api.models.pedido import Pedido
from api.models.entrada import Entrada
from api.models.venda import Venda


class ProviderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Fornecedor.objects.all()
    serializer_class = ProviderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Produto.objects.all()
    serializer_class = ProductSerializer


class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Venda.objects.all()
    serializer_class = SaleSerializer


class StockHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Historico.objects.all()
    serializer_class = HistorySerializer


class OrderBuyViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Pedido.objects.all()
    serializer_class = OrderSerializer


class EntryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Entrada.objects.all()
    serializer_class = EntrySerializer


class StockCurrentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Estoque.objects.all()
    serializer_class = StockSerializer
