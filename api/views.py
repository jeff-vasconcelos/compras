from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from api.serializer import ProdutoSerializer
from api.models import Produto

""" Views responsavel por todos os metodos de produtos """
class ProdutoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
