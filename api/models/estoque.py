from django.db import models
from api.models.fornecedor import Fornecedor
from core.models.empresas_models import Empresa, Filial
from api.models.produto import Produto


class Estoque(models.Model):
    cod_produto = models.IntegerField(null=False, blank=False)
    cod_filial = models.IntegerField(null=False, blank=False)
    cod_fornecedor = models.IntegerField(null=False, blank=False)
    qt_geral = models.FloatField(null=False, blank=False)
    qt_indenizada = models.FloatField(null=False, blank=False)
    qt_reservada = models.FloatField(null=False, blank=False)
    qt_pendente = models.FloatField(null=False, blank=False)
    qt_bloqueada = models.FloatField(null=False, blank=False)
    qt_disponivel = models.FloatField(null=False, blank=False)
    preco_venda = models.FloatField(null=False, blank=False)
    custo_ult_entrada = models.FloatField(null=False, blank=False)
    data = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto_estoqueatual',
                                blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_estoqueatual',
                                   blank=True, null=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='filial_estoqueatual')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_estoqueatual',
                                blank=True, null=True)
    
    campo_um = models.CharField(max_length=255, null=True, blank=True)
    campo_dois = models.CharField(max_length=255, null=True, blank=True)
    campo_tres = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoque'

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
        return self.produto.desc_produto
