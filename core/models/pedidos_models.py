from django.db import models
from core.models.empresas_models import Empresa


class PedidoInsight(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    desc_produto = models.CharField(max_length=255, null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    preco = models.CharField(max_length=255, null=True, blank=True)
    quantidade = models.CharField(max_length=255, null=True, blank=True)

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='pedidos_insight',
                                blank=True, null=True)

    campo_um = models.CharField(max_length=255, blank=True, null=True)
    campo_dois = models.CharField(max_length=255, blank=True, null=True)
    campo_tres = models.CharField(max_length=255, blank=True, null=True)
    campo_quatro = models.CharField(max_length=255, blank=True, null=True)
    campo_cinco = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.empresa.nome_fantasia
