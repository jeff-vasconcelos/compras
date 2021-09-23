from datetime import date, timedelta
from rest_framework import viewsets, generics

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.permissions import IsAuthenticated
from api.serializer import *

from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque_atual import Estoque
from api.models.historico_estoque import HistoricoEstoque
from api.models.pedido_compra import Pedido
from api.models.ultima_entrada import Entrada
from api.models.venda import Venda
from api.models.pedidos import Pedidos_API

from django.db.models import Q


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


def valida_pedidos_excluidos(id_empresa):

    global pedidos
    pedidos_existentes = Pedidos_API.objects.filter(empresa__id=id_empresa)
    lista_ids = []

    if pedidos_existentes:
        for i in pedidos_existentes:
            lista_ids.append(i.num_pedido)

        existe = list(set(lista_ids))

        hoje = date.today()
        ontem = date.today() - timedelta(1)

        pedidos = Pedido.objects.filter(
            empresa__id=id_empresa
        ).exclude(Q(num_pedido__in=existe) | Q(created_at=hoje) | Q(created_at=ontem))

        if pedidos:
            for p in pedidos:
                p.delete()

    return None
