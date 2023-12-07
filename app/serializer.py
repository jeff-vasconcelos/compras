from rest_framework import serializers

from app.models.produto import Produto
from app.models.fornecedor import Fornecedor
from app.models.estoque import Estoque
from app.models.historico import Historico
from app.models.pedido import Pedido
from app.models.entrada import Entrada
from app.models.venda import Venda
from app.validator import (ValidatesDataExists,
                           ProviderCheckUpdate,
                           ProductCheckUpdate,
                           OrderCheckUpdate,
                           StockCheckUpdate)


# class ProviderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Fornecedor
#         fields = '__all__'
#
#     def validate(self, data):
#         query = ValidExistsData.provider_exists(data)
#         if query:
#             ProviderCheckUpdate.check_provider_data(data, query)
#             raise serializers.ValidationError({'message': "provider already exists"})
#
#         return data
#

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Produto
#         fields = '__all__'
#
#     def validate(self, data):
#         if not ValidExistsData.provider_exists(data):
#             raise serializers.ValidationError({'message': "provider does not exists"})
#
#         query = ValidExistsData.product_exists(data)
#         if query:
#             ProductCheckUpdate.check_product_data(data, query)
#             raise serializers.ValidationError({'message': "product already exists"})
#
#         return data


# class SaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Venda
#         fields = '__all__'
#
#     def validate(self, data):
#         if not ValidExistsData.provider_exists(data):
#             raise serializers.ValidationError({'message': "provider does not exists"})
#
#         if not ValidExistsData.branch_exists(data):
#             raise serializers.ValidationError({'message': "branch does not exists"})
#
#         if not ValidExistsData.product_exists(data):
#             raise serializers.ValidationError({'message': "product does not exists"})
#
#         if ValidExistsData.sale_exists(data):
#             raise serializers.ValidationError({'message': "registry already exists"})
#
#         return data


# class HistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Historico
#         fields = '__all__'
#
#     def validate(self, data):
#         if not ValidExistsData.provider_exists(data):
#             raise serializers.ValidationError({'message': "provider does not exists"})
#
#         if not ValidExistsData.branch_exists(data):
#             raise serializers.ValidationError({'message': "branch does not exists"})
#
#         if not ValidExistsData.product_exists(data):
#             raise serializers.ValidationError({'message': "product does not exists"})
#
#         if ValidExistsData.history_exists(data):
#             raise serializers.ValidationError({'message': "registry already exists"})
#
#         return data


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pedido
#         fields = '__all__'
#
#     def validate(self, data):
#         if not ValidatesDataExists.provider_exists(data):
#             raise serializers.ValidationError({'message': "provider does not exists"})
#
#         if not ValidatesDataExists.branch_exists(data):
#             raise serializers.ValidationError({'message': "branch does not exists"})
#
#         if not ValidatesDataExists.product_exists(data):
#             raise serializers.ValidationError({'message': "product does not exists"})
#
#         query = ValidatesDataExists.order_exists(data)
#         if query:
#             OrderCheckUpdate.check_order_data(data, query)
#             raise serializers.ValidationError({'message': "registry already exists"})
#
#         return data
#

# class EntrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Entrada
#         fields = '__all__'
#
#     def validate(self, data):
#
#         if not ValidExistsData.provider_exists(data):
#             raise serializers.ValidationError({'message': "provider does not exists"})
#
#         if not ValidExistsData.branch_exists(data):
#             raise serializers.ValidationError({'message': "branch does not exists"})
#
#         if not ValidExistsData.product_exists(data):
#             raise serializers.ValidationError({'message': "product already exists"})
#
#         if ValidExistsData.entry_exists(data):
#             raise serializers.ValidationError({'message': "registry already exists"})
#
#         return data


# class StockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Estoque
#         fields = '__all__'
#
#     def validate(self, data):
#         if not ValidatesDataExists.provider_exists(data):
#             raise serializers.ValidationError({'message': "provider does not exists"})
#
#         if not ValidatesDataExists.branch_exists(data):
#             raise serializers.ValidationError({'message': "branch does not exists"})
#
#         if not ValidatesDataExists.product_exists(data):
#             raise serializers.ValidationError({'message': "product does not exists"})
#
#         query = ValidatesDataExists.stock_exists(data)
#         if query:
#             StockCheckUpdate.check_stock_data(data, query)
#             raise serializers.ValidationError({'message': "registry already exists"})
#
#         return data