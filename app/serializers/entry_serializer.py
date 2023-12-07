from rest_framework import serializers

from app.models import Entrada
from app.validator import ValidatesDataExists


class EntryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'


class EntryIntegrationSerializer(EntryBaseSerializer):
    class Meta(EntryBaseSerializer.Meta):
        ordering = ['-id']


class EntrySerializer(EntryBaseSerializer):
    class Meta(EntryBaseSerializer.Meta):
        pass

    def validate(self, data):
        if ValidatesDataExists.entry_exists(data):
            raise serializers.ValidationError({'message': "registry already exists"})

        if not ValidatesDataExists.provider_exists(data):
            raise serializers.ValidationError({'message': "provider does not exists"})

        if not ValidatesDataExists.branch_exists(data):
            raise serializers.ValidationError({'message': "branch does not exists"})

        if not ValidatesDataExists.product_exists(data):
            raise serializers.ValidationError({'message': "product already exists"})

        return data
