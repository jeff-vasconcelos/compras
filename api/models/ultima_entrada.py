from django.db import models
from api.models.fornecedor import Fornecedor
from core.models.empresas_models import Empresa, Filial
from api.models.produto import Produto


class UltimaEntrada(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    desc_produto = models.CharField(max_length=255, null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, null=True, blank=True, related_name='filial_ultimaentrada')
    cod_fornecedor = models.IntegerField(null=True, blank=True)

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto_ultimaentrada',
                                blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecedor_ultimaentrada',
                                   blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_ultimaentrada',
                                blank=True, null=True)
    qt_ult_entrada = models.IntegerField(null=True, blank=True)
    vl_ult_entrada = models.FloatField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Ultima entrada'
        verbose_name_plural = 'Ultimas entradas'

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
        return self.desc_produto