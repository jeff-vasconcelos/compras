from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.serializer import *
from app.models.produto import Produto
from app.models.fornecedor import Fornecedor
from app.models.estoque import Estoque
from app.models.historico import Historico
from app.models.pedido import Pedido
from app.models.entrada import Entrada
from app.models.venda import Venda




