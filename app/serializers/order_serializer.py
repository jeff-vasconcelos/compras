from rest_framework import serializers

from app.models import Pedido
from app.validator import ValidatesDataExists, OrderCheckUpdate


class OrderBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class OrderIntegrationSerializer(OrderBaseSerializer):
    class Meta(OrderBaseSerializer.Meta):
        ordering = ['-id']


class OrdersGetSerializer(OrderBaseSerializer):
    class Meta(OrderBaseSerializer.Meta):
        fields = ['num_pedido',
                  'cod_produto',
                  'cod_filial',
                  'saldo',
                  'data']


class OrderSerializer(OrderBaseSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

    def validate(self, data):
        if not ValidatesDataExists.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if not ValidatesDataExists.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if not ValidatesDataExists.product_exists(data):
            raise serializers.ValidationError({'message': "product does not exists"})

        query = ValidatesDataExists.order_exists(data)
        if query:
            OrderCheckUpdate.check_order_data(data, query)
            raise serializers.ValidationError({'message': "registry already exists"})

        return data
