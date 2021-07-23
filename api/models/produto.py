from django.db import models
from core.models.empresas_models import Empresa
from api.models.fornecedor import Fornecedor


class Produto(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    desc_produto = models.CharField(max_length=255, null=True, blank=True)
    embalagem = models.CharField(max_length=255, null=True, blank=True)
    quantidade_un_cx = models.FloatField(blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)
    peso_liquido = models.CharField(max_length=255, blank=True, null=True)
    principio_ativo = models.CharField(max_length=255, null=True, blank=True)
    cod_fabrica = models.IntegerField(null=True, blank=True)
    cod_ncm = models.CharField(max_length=255, null=True, blank=True)
    cod_auxiliar = models.IntegerField(null=True, blank=True)
    cod_depto = models.IntegerField(null=True, blank=True)
    cod_sec = models.IntegerField(null=True, blank=True)
    desc_departamento = models.CharField(max_length=255, null=True, blank=True)
    desc_secao = models.CharField(max_length=255, null=True, blank=True)

    cod_fornecedor = models.IntegerField(null=True, blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_produto',
                                blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produto',
                                blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.fornecedor:
            fornecedor = Fornecedor.objects.get(cod_fornecedor=self.cod_fornecedor, empresa=self.empresa)
            self.fornecedor = fornecedor
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cod_produto} - {self.desc_produto} - {self.empresa.razao_social}'
