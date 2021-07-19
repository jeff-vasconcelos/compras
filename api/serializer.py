from rest_framework import serializers
from api.validator import *
from api.models.produto import *
from api.models.estoque_atual import *
from api.models.historico_estoque import *
from api.models.pedido_compra import *
from api.models.ultima_entrada import *
from api.models.venda import *


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

    def validate(self, data):
        if not valida_produto(data):
            raise serializers.ValidationError({'produto': "registro já existe!"})

        fornecedor = data['cod_fornecedor']
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor)

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
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto)

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
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto)

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
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto)

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
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto)

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
        fornec = Fornecedor.objects.filter(cod_fornecedor=fornecedor)

        produto = data['cod_produto']
        produt = Produto.objects.filter(cod_produto=produto)

        if not fornec:
            raise serializers.ValidationError({'fornecedor': "registro não existente"})

        if not produt:
            raise serializers.ValidationError({'produto': "registro não existente"})

        return data