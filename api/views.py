from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from api.serializer import *
from api.models.produto_models import *
from api.models.avarias_models import *
from api.models.estoque_atual_models import *
from api.models.hist_estoque_models import *
from api.models.p_compras_models import *
from api.models.ultima_entrada_models import *
from api.models.vendas_models import *


class ProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class FornecedorViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer


class AvariaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Avaria.objects.all()
    serializer_class = AvariaSerializer


class EstoqueAtualViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = EstoqueAtual.objects.all()
    serializer_class = EstoqueAtualSerializer


class HistEstoqueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = HistEstoque.objects.all()
    serializer_class = HistEstoqueSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = PedidoCompras.objects.all()
    serializer_class = PedidoSerializer


class UltEntradaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UltimaEntrada.objects.all()
    serializer_class = UltEntradaSerializer


class VendaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Venda.objects.all()
    serializer_class = VendasSerializer

