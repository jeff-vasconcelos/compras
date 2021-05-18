from django.db import models
from api.models.fornecedor_models import Fornecedor
from core.models.empresas_models import Empresa
from api.models.produto_models import Produto


class Venda(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    cod_fornecedor = models.IntegerField(null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto_vendas',
                                blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_vendas',
                                   blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_vendas',
                                blank=True, null=True)
    qt_vendas = models.IntegerField(null=True, blank=True)
    preco_unit = models.IntegerField(null=True, blank=True)
    custo_fin = models.IntegerField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.cod_produto} - {self.empresa.razao_social}'