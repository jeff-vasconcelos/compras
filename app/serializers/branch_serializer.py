from rest_framework import serializers

from core.models.empresas_models import Filial


class BranchBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = '__all__'


class BranchesSerializer(BranchBaseSerializer):
    class Meta(BranchBaseSerializer.Meta):
        ordering = ['-id']


class BranchesGetSerializer(BranchBaseSerializer):
    class Meta(BranchBaseSerializer.Meta):
        fields = ['cod_filial', ]
