from rest_framework import serializers

from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque import Estoque
from api.models.historico import Historico
from api.models.pedido import Pedido
from api.models.entrada import Entrada
from api.models.venda import Venda
from core.models.empresas_models import Filial


class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'
        ordering = ['-id']


class ProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        ordering = ['-id']


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        ordering = ['-id']


class HistoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'
        ordering = ['-id']


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'
        ordering = ['-id']


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        ordering = ['-id']


class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'
        ordering = ['-id']


class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'
        ordering = ['-id']


class ProvidersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['cod_fornecedor', ]


class BranchesGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = ['cod_filial', ]


class ProductsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['cod_produto', ]


class OrdersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['num_pedido',
                  'cod_produto',
                  'cod_filial',
                  'saldo',
                  'data']


class StockGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = ['cod_produto',
                  'cod_filial',
                  'qt_geral',
                  'qt_disponivel']