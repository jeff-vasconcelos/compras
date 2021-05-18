from rest_framework import serializers
from api.validator import *
from api.models.produto_models import *
from api.models.avarias_models import *


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


class AvariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaria
        fields = '__all__'

    def validate(self, data):
        if not valida_avaria(data):
            raise serializers.ValidationError({'avaria': "registro já existe!"})

        return data