from django.db import models
from api.models.fornecedor_models import Fornecedor
from core.models.empresas_models import Empresa
from api.models.produto_models import Produto


class HistEstoque(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    cod_fornecedor = models.IntegerField(null=True, blank=True)

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto_histestoque',
                                blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_histestoque',
                                   blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_histestoque',
                                blank=True, null=True)
    qt_estoque = models.IntegerField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Histórico de estoque'
        verbose_name_plural = 'Históricos de estoque'

    def __str__(self):
        return self.cod_produto