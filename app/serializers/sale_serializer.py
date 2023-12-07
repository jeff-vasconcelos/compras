from rest_framework import serializers

from app.models import Venda
from app.validator import ValidatesDataExists


class SaleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'


class SaleIntegrationSerializer(SaleBaseSerializer):
    class Meta(SaleBaseSerializer.Meta):
        ordering = ['-id']


class SaleSerializer(SaleBaseSerializer):
    class Meta(SaleBaseSerializer.Meta):
        pass

    def validate(self, data):
        if not ValidatesDataExists.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if not ValidatesDataExists.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if not ValidatesDataExists.product_exists(data):
            raise serializers.ValidationError({'message': "product does not exists"})

        if ValidatesDataExists.sale_exists(data):
            raise serializers.ValidationError({'message': "registry already exists"})

        return data
