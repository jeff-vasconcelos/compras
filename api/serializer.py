from rest_framework import serializers
from api.validator import *

from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque_atual import Estoque
from api.models.historico_estoque import HistoricoEstoque
from api.models.pedido_compra import Pedido
from api.models.ultima_entrada import Entrada
from api.models.venda import Venda

from api.models.pedidos import Pedidos_API


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

    def validate(self, data):
        if not valida_produto(data):
            raise serializers.ValidationError({'produto': "registro já existe!"})

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)

        if not fornec:
            raise serializers.ValidationError({'fornecedor': "registro não existente"})

        return data


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

    def validate(self, data):
        if not valida_fornecedor(data):
            raise serializers.ValidationError({'fornecedor': "registro ja existente"})

        return data


class EstoqueAtualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'

    def validate(self, data):
        if not valida_estoque_atual(data):
            raise serializers.ValidationError({'estoque atual': "registro já existe!"})

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not fornec:
            raise serializers.ValidationError({'fornecedor': "registro não existente"})

        if not produt:
            raise serializers.ValidationError({'produto': "registro não existente"})
        return data


class HistEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoEstoque
        fields = '__all__'

    def validate(self, data):
        if not valida_hist_estoque(data):
            raise serializers.ValidationError({'historico estoque': "registro já existe!"})

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not fornec:
            raise serializers.ValidationError({'fornecedor': "registro não existente"})

        if not produt:
            raise serializers.ValidationError({'produto': "registro não existente"})

        return data


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

    def validate(self, data):
        if not valida_pedido(data):
            raise serializers.ValidationError({'pedido de compra': "registro já existe!"})

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)

        produto = data['cod_produto']

        produt = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not fornec:
            raise serializers.ValidationError({'fornecedor': "registro não existente"})

        if not produt:
            raise serializers.ValidationError({'produto': "registro não existente"})

        return data


class UltEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'

    def validate(self, data):
        if not valida_ultentrada(data):
            raise serializers.ValidationError({'ultima entrada': "registro já existe!"})

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not fornec:
            raise serializers.ValidationError({'fornecedor': "registro não existente"})

        if not produt:
            raise serializers.ValidationError({'produto': "registro não existente"})
        return data


class VendasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'

    def validate(self, data):

        if not valida_venda(data):
            raise serializers.ValidationError({'venda': "registro já existe!"})

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not fornec:
            raise serializers.ValidationError({'fornecedor': "registro não existente"})

        if not produt:
            raise serializers.ValidationError({'produto': "registro não existente"})

        return data