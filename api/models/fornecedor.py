from django.db import models
from core.models.empresas_models import Empresa


class Fornecedor(models.Model):
    cod_fornecedor = models.IntegerField(null=False, blank=False)
    desc_fornecedor = models.CharField(max_length=255, null=False, blank=False)
    cnpj = models.CharField(max_length=255, null=True, blank=True)
    iestadual = models.CharField(max_length=255, null=True, blank=True)
    leadtime = models.IntegerField(null=True, blank=True)
    ciclo_reposicao = models.IntegerField(null=True, blank=True)
    tempo_estoque = models.IntegerField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='fonecedor_empresa',
                                blank=True, null=True)
    
    # campo_um = models.CharField(max_length=255, null=True, blank=True)
    # campo_dois = models.CharField(max_length=255, null=True, blank=True)
    # campo_tres = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedor'

    def save(self, *args, **kwargs):
        if not self.leadtime:
            leadtime = 25
            ciclo_reposicao = 30
            tempo_estoque = 55

            self.leadtime = leadtime
            self.ciclo_reposicao = ciclo_reposicao
            self.tempo_estoque = tempo_estoque

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cod_fornecedor} - {self.desc_fornecedor}'
