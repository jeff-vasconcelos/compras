from rest_framework import serializers
from api.validator import *
from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque import Estoque
from api.models.historico import Historico
from api.models.pedido import Pedido
from api.models.entrada import Entrada
from api.models.venda import Venda
from api.models.pedido_duplicado import PedidoDuplicado
from core.models.empresas_models import Filial, Empresa


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
            raise serializers.ValidationError({'fornecedor': "nao cadastrado"})

        return data


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

    def validate(self, data):
        if not valida_fornecedor(data):
            raise serializers.ValidationError({'fornecedor': "registro ja existe"})

        return data


class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'

    def validate(self, data):

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        produto = data['cod_produto']
        filial = data['cod_filial']

        qs_fornecedor = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)
        qs_filial = Filial.objects.filter(cod_filial=filial, empresa=empresa)
        qs_produto = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not qs_fornecedor:
            raise serializers.ValidationError({'fornecedor': "nao cadastrado"})

        if not qs_produto:
            raise serializers.ValidationError({'produto': "nao cadastrado"})

        if not qs_filial:
            raise serializers.ValidationError({'filial': "nao cadastrada"})

        if not valida_estoque_atual(data):
            raise serializers.ValidationError({'estoque atual': "registro ja existe!"})

        return data


class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'

    def validate(self, data):

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        produto = data['cod_produto']
        filial = data['cod_filial']

        qs_fornecedor = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)
        qs_filial = Filial.objects.filter(cod_filial=filial, empresa=empresa)
        qs_produto = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not qs_fornecedor:
            raise serializers.ValidationError({'fornecedor': "nao cadastrado"})

        if not qs_produto:
            raise serializers.ValidationError({'produto': "nao cadastrado"})

        if not qs_filial:
            raise serializers.ValidationError({'filial': "nao cadastrada"})

        if not valida_hist_estoque(data):
            raise serializers.ValidationError({'historico estoque': "registro ja existe!"})

        return data


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

    def validate(self, data):

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        produto = data['cod_produto']
        filial = data['cod_filial']

        qs_fornecedor = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)
        qs_filial = Filial.objects.filter(cod_filial=filial, empresa=empresa)
        qs_produto = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not qs_fornecedor:
            raise serializers.ValidationError({'fornecedor': "nao cadastrado"})

        if not qs_produto:
            raise serializers.ValidationError({'produto': "nao cadastrado"})

        if not qs_filial:
            raise serializers.ValidationError({'filial': "nao cadastrada"})

        if not valida_pedido(data):
            raise serializers.ValidationError({'pedido de compra': "registro ja existe!"})

        return data


class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'

    def validate(self, data):

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        produto = data['cod_produto']
        filial = data['cod_filial']

        qs_fornecedor = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)
        qs_filial = Filial.objects.filter(cod_filial=filial, empresa=empresa)
        qs_produto = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not qs_fornecedor:
            raise serializers.ValidationError({'fornecedor': "nao cadastrado"})

        if not qs_produto:
            raise serializers.ValidationError({'produto': "nao cadastrado"})

        if not qs_filial:
            raise serializers.ValidationError({'filial': "nao cadastrada"})

        if not valida_ultentrada(data):
            raise serializers.ValidationError({'ultima entrada': "registro ja existe!"})

        return data


class VendasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'

    def validate(self, data):

        fornecedor = data['cod_fornecedor']
        empresa = data['empresa']
        produto = data['cod_produto']
        filial = data['cod_filial']

        qs_fornecedor = Fornecedor.objects.filter(cod_fornecedor=fornecedor, empresa=empresa)
        qs_filial = Filial.objects.filter(cod_filial=filial, empresa=empresa)
        qs_produto = Produto.objects.filter(cod_produto=produto, empresa=empresa)

        if not qs_fornecedor:
            raise serializers.ValidationError({'fornecedor': "nao cadastrada"})

        if not qs_produto:
            raise serializers.ValidationError({'produto': "nao cadastrada"})

        if not qs_filial:
            raise serializers.ValidationError({'filial': "nao cadastrada"})

        if not valida_venda(data):
            raise serializers.ValidationError({'venda': "registro ja existe!"})

        return data