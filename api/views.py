from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from api.serializer import *

from api.models.produto import *
from api.models.estoque_atual import *
from api.models.historico_estoque import *
from api.models.pedido_compra import *
from api.models.ultima_entrada import *
from api.models.venda import *



class ProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class FornecedorViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer


class EstoqueAtualViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Estoque.objects.all()
    serializer_class = EstoqueAtualSerializer


class HistEstoqueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = HistoricoEstoque.objects.all()
    serializer_class = HistEstoqueSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class UltEntradaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Entrada.objects.all()
    serializer_class = UltEntradaSerializer


class VendaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Venda.objects.all()
    serializer_class = VendasSerializer

