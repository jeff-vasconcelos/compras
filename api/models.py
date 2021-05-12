from django.db import models
from core.models.empresas_models import Empresa


class Fornecedor(models.Model):
    cod_fornecedor = models.IntegerField(null=True, blank=True)
    desc_fornecedor = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='fonecedor_empresa',
                                blank=True, null=True)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedor'

    def __str__(self):
        return self.desc_fornecedor


""" Modelo de produtos """
class Produto(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    desc_produto = models.CharField(max_length=255, null=True, blank=True)
    embalagem = models.CharField(max_length=255, null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    cod_fornec = models.IntegerField(null=True, blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_produto',
                                blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produto',
                                blank=True, null=True)

    def __str__(self):
        return self.desc_produto


""" Modelo de parametros """
class Parametro(models.Model):
    meta_compras = models.IntegerField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='parametros',
                                blank=True, null=True)

    def __str__(self):
        return self.meta_compras
