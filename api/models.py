from django.db import models
from core.models.empresas_models import Empresa

""" Modelo de produtos """
class Produto(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    desc_produto = models.CharField(max_length=255, null=True, blank=True)
    embalagem = models.CharField(max_length=255, null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    cod_fornec = models.IntegerField(null=True, blank=True)
    qt_venda = models.IntegerField(null=True, blank=True)
    qt_avaria = models.IntegerField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
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