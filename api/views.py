
from rest_framework import viewsets, generics
from api.serializer import ProdutoSerializer
from api.models import Produto

""" Views responsavel por todos os metodos de produtos """
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
