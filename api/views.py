from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from api.serializer import *
from api.models.produto_models import Produto
from api.models.fornecedor_models import Fornecedor


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
