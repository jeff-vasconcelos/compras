from rest_framework import serializers

from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque import Estoque
from api.models.historico import Historico
from api.models.pedido import Pedido
from api.models.entrada import Entrada
from api.models.venda import Venda
from api.validator import (ValidExistsData,
                           ProviderCheckUpdate,
                           ProductCheckUpdate,
                           OrderCheckUpdate,
                           StockCheckUpdate)


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

    def validate(self, data):
        query = ValidExistsData.provider_exists(data)
        if query:
            ProviderCheckUpdate.check_provider_data(data, query)
            raise serializers.ValidationError({'message': "provider already exists"})

        return data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

    def validate(self, data):
        if not ValidExistsData.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        query = ValidExistsData.product_exists(data)
        if query:
            ProductCheckUpdate.check_product_data(data, query)
            raise serializers.ValidationError({'message': "product already exists"})

        return data


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'

    def validate(self, data):
        if not ValidExistsData.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if ValidExistsData.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if ValidExistsData.product_exists(data):
            raise serializers.ValidationError({'message': "product already exists"})

        if ValidExistsData.sale_exists(data):
            raise serializers.ValidationError({'message': "registry already exists"})

        return data


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'

    def validate(self, data):
        if not ValidExistsData.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if ValidExistsData.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if ValidExistsData.product_exists(data):
            raise serializers.ValidationError({'message': "product already exists"})

        if ValidExistsData.history_exists(data):
            raise serializers.ValidationError({'message': "registry already exists"})

        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

    def validate(self, data):
        if not ValidExistsData.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if ValidExistsData.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if ValidExistsData.product_exists(data):
            raise serializers.ValidationError({'message': "product already exists"})

        query = ValidExistsData.order_exists(data)
        if query:
            OrderCheckUpdate.check_order_data(data, query)
            raise serializers.ValidationError({'message': "registry already exists"})

        return data


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'

    def validate(self, data):

        if not ValidExistsData.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if ValidExistsData.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if ValidExistsData.product_exists(data):
            raise serializers.ValidationError({'message': "product already exists"})

        if ValidExistsData.entry_exists(data):
            raise serializers.ValidationError({'message': "registry already exists"})

        return data


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'

    def validate(self, data):
        if not ValidExistsData.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if ValidExistsData.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if ValidExistsData.product_exists(data):
            raise serializers.ValidationError({'message': "product already exists"})

        query = ValidExistsData.stock_exists(data)
        if query:
            StockCheckUpdate.check_stock_data(data, query)
            raise serializers.ValidationError({'message': "registry already exists"})

        return data