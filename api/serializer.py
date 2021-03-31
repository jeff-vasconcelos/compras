from rest_framework import serializers
from api.validator import *
from api.models import *

""" Serializador de produtos """
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

    """ Função responsável por chamar e enviar dados ao validator """
    def validate(self, data):
        if not valida_produto(data):
            raise serializers.ValidationError({'produto':"registro ja existente"})

        return data