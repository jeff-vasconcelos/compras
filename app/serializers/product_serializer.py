from rest_framework import serializers

from app.models import Produto
from app.validator import ValidatesDataExists, ProductCheckUpdate


class ProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'


class ProductIntegrationSerializer(ProductBaseSerializer):
    class Meta(ProductBaseSerializer.Meta):
        ordering = ['-id']


class ProductsGetSerializer(ProductBaseSerializer):
    class Meta(ProductBaseSerializer.Meta):
        fields = ['cod_produto', ]


class ProductSerializer(ProductBaseSerializer):
    class Meta(ProductBaseSerializer.Meta):
        pass

    def validate(self, data):
        if not ValidatesDataExists.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        query = ValidatesDataExists.product_exists(data)
        if query:
            ProductCheckUpdate.check_product_data(data, query)
            raise serializers.ValidationError({'message': "product already exists"})

        return data
