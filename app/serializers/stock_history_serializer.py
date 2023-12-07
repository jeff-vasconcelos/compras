from rest_framework import serializers

from app.models import Historico
from app.validator import ValidatesDataExists


class HistoryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'


class HistoryIntegrationSerializer(HistoryBaseSerializer):
    class Meta(HistoryBaseSerializer.Meta):
        ordering = ['-id']


class HistorySerializer(HistoryBaseSerializer):
    class Meta(HistoryBaseSerializer.Meta):
        pass

    def validate(self, data):
        if not ValidatesDataExists.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if not ValidatesDataExists.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if not ValidatesDataExists.product_exists(data):
            raise serializers.ValidationError({'message': "product does not exists"})

        if ValidatesDataExists.history_exists(data):
            raise serializers.ValidationError({'message': "registry already exists"})

        return data
