from rest_framework import serializers
from api.validator import *
from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque_atual import Estoque
from api.models.historico_estoque import HistoricoEstoque
from api.models.pedido_compra import Pedido
from api.models.ultima_entrada import Entrada
from api.models.venda import Venda


class FornecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'


class ProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'


class HistSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoEstoque
        fields = '__all__'


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'


class PedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class EntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'


class EstSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'