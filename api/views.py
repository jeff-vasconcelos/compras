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
    serializer_class = EstoqueSerializer


class HistEstoqueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class UltEntradaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Entrada.objects.all()
    serializer_class = EntradaSerializer


class VendaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Venda.objects.all()
    serializer_class = VendasSerializer
