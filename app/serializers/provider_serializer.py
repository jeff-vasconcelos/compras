from rest_framework import serializers

from app.models import Fornecedor
from app.validator import ValidatesDataExists, ProviderCheckUpdate


class ProviderBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'


class ProviderIntegrationSerializer(ProviderBaseSerializer):
    class Meta(ProviderBaseSerializer.Meta):
        ordering = ['-id']


class ProvidersGetSerializer(ProviderBaseSerializer):
    class Meta(ProviderBaseSerializer.Meta):
        fields = ['cod_fornecedor', ]


class ProviderSerializer(ProviderBaseSerializer):
    class Meta(ProviderBaseSerializer.Meta):
        pass

    def validate(self, data):
        query = ValidatesDataExists.provider_exists(data)
        if query:
            ProviderCheckUpdate.check_provider_data(data, query)
            raise serializers.ValidationError({'message': "provider already exists"})

        return data
