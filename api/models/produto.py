from django.db import models
from core.models.empresas_models import Empresa
from api.models.fornecedor import Fornecedor


class Produto(models.Model):
    cod_produto = models.IntegerField(null=False, blank=False)
    desc_produto = models.CharField(max_length=255, null=False, blank=False)
    embalagem = models.CharField(max_length=255, null=True, blank=True)
    quantidade_un_cx = models.FloatField(null=False, blank=False)
    marca = models.CharField(max_length=255, null=True, blank=True)
    peso_liquido = models.CharField(max_length=255, null=True, blank=True)
    principio_ativo = models.CharField(max_length=255, null=True, blank=True)
    cod_fabrica = models.IntegerField(null=True, blank=True)
    cod_ncm = models.CharField(max_length=255, null=True, blank=True)
    cod_auxiliar = models.IntegerField(null=True, blank=True)
    cod_depto = models.IntegerField(null=True, blank=True)
    cod_sec = models.IntegerField(null=True, blank=True)
    desc_departamento = models.CharField(max_length=255, null=True, blank=True)
    desc_secao = models.CharField(max_length=255, null=True, blank=True)
    cod_fornecedor = models.IntegerField(null=False, blank=False)
    
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_produto',
                                blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produto',
                                blank=True, null=True)
    
    campo_um = models.CharField(max_length=255, null=True, blank=True)
    campo_dois = models.CharField(max_length=255, null=True, blank=True)
    campo_tres = models.CharField(max_length=255, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.fornecedor:
            fornecedor = Fornecedor.objects.get(cod_fornecedor=self.cod_fornecedor, empresa=self.empresa)
            self.fornecedor = fornecedor
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cod_produto} - {self.desc_produto} - {self.empresa.razao_social}'
