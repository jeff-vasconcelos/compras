from django.db import models
from api.models.fornecedor import Fornecedor
from core.models.empresas_models import Empresa, Filial
from api.models.produto import Produto


class Venda(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    desc_produto = models.CharField(max_length=255, null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, null=True, blank=True, related_name='filial_venda')
    cod_fornecedor = models.IntegerField(null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto_venda',
                                blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_venda',
                                   blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_venda',
                                blank=True, null=True)
    qt_vendas = models.IntegerField(null=True, blank=True)
    qt_unit_caixa = models.IntegerField(null=True, blank=True)
    preco_unit = models.FloatField(null=True, blank=True)
    custo_fin = models.FloatField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    cliente = models.CharField(max_length=255, null=True, blank=True)
    marca = models.CharField(max_length=255, null=True, blank=True)
    peso_liquido = models.FloatField(null=True, blank=True)
    cod_depto = models.IntegerField(null=True, blank=True)
    num_nota = models.IntegerField(null=True, blank=True)
    cod_usur = models.IntegerField(null=True, blank=True)
    cod_fab = models.IntegerField(null=True, blank=True)
    desc_dois = models.CharField(max_length=255, null=True, blank=True)
    supervisor = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.fornecedor:
            fornecedor = Fornecedor.objects.get(cod_fornecedor=self.cod_fornecedor, empresa=self.empresa)
            produto = Produto.objects.get(cod_produto=self.cod_produto, empresa=self.empresa)
            filial = Filial.objects.get(cod_filial=self.cod_filial, empresa=self.empresa)
            self.fornecedor = fornecedor
            self.produto = produto
            self.filial = filial

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cod_produto} - {self.empresa.razao_social}'