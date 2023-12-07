from rest_framework import serializers

from app.models import Estoque
from app.validator import ValidatesDataExists, StockCheckUpdate


class StockBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'


class StockIntegrationSerializer(StockBaseSerializer):
    class Meta(StockBaseSerializer.Meta):
        ordering = ['-id']


class StockSerializer(StockBaseSerializer):
    class Meta(StockBaseSerializer.Meta):
        pass

    def validate(self, data):
        if not ValidatesDataExists.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if not ValidatesDataExists.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if not ValidatesDataExists.product_exists(data):
            raise serializers.ValidationError({'message': "product does not exists"})

        query = ValidatesDataExists.stock_exists(data)
        if query:
            StockCheckUpdate.check_stock_data(data, query)
            raise serializers.ValidationError({'message': "registry already exists"})

        return data
