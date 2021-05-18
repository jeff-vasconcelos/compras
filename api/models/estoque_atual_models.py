from django.db import models
from api.models.fornecedor_models import Fornecedor
from core.models.empresas_models import Empresa
from api.models.produto_models import Produto


class EstoqueAtual(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    desc_produto = models.CharField(max_length=255, null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    cod_fornecedor = models.IntegerField(null=True, blank=True)

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto_estoqueatual',
                                blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_estoqueatual',
                                   blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_estoqueatual',
                                blank=True, null=True)
    qt_estoque_geral = models.IntegerField(null=True, blank=True)
    qt_indenizada = models.IntegerField(null=True, blank=True)
    qt_reservada = models.IntegerField(null=True, blank=True)
    qt_pendente = models.IntegerField(null=True, blank=True)
    qt_disponivel = models.IntegerField(null=True, blank=True)
    custo_ult_ent = models.FloatField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Estoque atual'
        verbose_name_plural = 'Estoque atual'

    def save(self, *args, **kwargs):
        if not self.fornecedor:
            fornecedor = Fornecedor.objects.get(cod_fornecedor=self.cod_fornecedor, empresa=self.empresa)
            produto = Produto.objects.get(cod_produto=self.cod_produto, empresa=self.empresa)
            self.fornecedor = fornecedor
            self.produto = produto

        super().save(*args, **kwargs)

    def __str__(self):
        return self.desc_produto