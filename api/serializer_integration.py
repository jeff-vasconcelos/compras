from rest_framework import serializers
from api.validator import *
from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque import Estoque
from api.models.historico import Historico
from api.models.pedido import Pedido
from api.models.entrada import Entrada
from api.models.venda import Venda
from core.models.empresas_models import Filial


class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'
        ordering = ['-id']


class FornecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        ordering = ['-id']


class ProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        ordering = ['-id']


class HistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'
        ordering = ['-id']


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'
        ordering = ['-id']


class PedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        ordering = ['-id']


class EntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'
        ordering = ['-id']


class EstSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'
        ordering = ['-id']