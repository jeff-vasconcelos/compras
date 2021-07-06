from django.db import models
from core.models.empresas_models import Empresa


class Fornecedor(models.Model):
    cod_fornecedor = models.IntegerField(null=True, blank=True)
    desc_fornecedor = models.CharField(max_length=255, null=True, blank=True)
    leadtime = models.IntegerField(null=True, blank=True)
    ciclo_reposicao = models.IntegerField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='fonecedor_empresa',
                                blank=True, null=True)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedor'

    def __str__(self):
        return self.desc_fornecedor