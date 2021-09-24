from rest_framework import serializers
from api.validator import *
from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque_atual import Estoque
from api.models.historico_estoque import HistoricoEstoque
from api.models.pedido_compra import Pedido
from api.models.ultima_entrada import Entrada
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
        model = HistoricoEstoque
        fields = '__all__'
        ordering = ['-id']

    # def validate(self, attrs):
    #
    #     cod_fornecedor = attrs['cod_fornecedor']
    #     cod_produto = attrs['cod_produto']
    #     cod_filial = attrs['cod_filial']
    #     quantidade = attrs['qt_estoque']
    #     date = attrs['data']
    #     empresa = attrs['empresa']
    #
    #     qs_fornecedor = Fornecedor.objects.filter(cod_fornecedor=cod_fornecedor,
    #                                               empresa=empresa)
    #
    #     qs_historico = HistoricoEstoque.objects.filter(
    #         cod_produto=cod_produto,
    #         cod_filial=cod_filial,
    #         empresa=empresa,
    #         qt_estoque=quantidade,
    #         data=date
    #     )
    #
    #     if not qs_fornecedor:
    #         raise serializers.ValidationError({'fornecedor': 'nao cadastrado'})
    #
    #     if qs_historico:
    #         raise serializers.ValidationError({'error': 'registro já existe'})
    #
    #     return attrs


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