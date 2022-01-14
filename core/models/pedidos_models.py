from django.db import models
from core.models.empresas_models import Empresa


class PedidoInsight(models.Model):
    numero = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='pedidos_insight',
                                blank=True, null=True)
    usuario = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name='Criado em:')

    campo_um = models.CharField(max_length=255, blank=True, null=True)
    campo_dois = models.CharField(max_length=255, blank=True, null=True)
    campo_tres = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Pedido Insight'
        verbose_name_plural = 'Pedidos Insight'

    def __str__(self):
        return f'{self.empresa.nome_fantasia} / {self.numero}'



class ItemPedidoInsight(models.Model):
    cod_produto = models.IntegerField(null=True, blank=True)
    desc_produto = models.CharField(max_length=255, null=True, blank=True)
    cod_filial = models.IntegerField(null=True, blank=True)
    preco = models.CharField(max_length=255, null=True, blank=True)
    quantidade = models.CharField(max_length=255, null=True, blank=True)

    pedido = models.ForeignKey(PedidoInsight, on_delete=models.CASCADE, related_name='pedidos_insight_itens',
                                blank=True, null=True)

    campo_um = models.CharField(max_length=255, blank=True, null=True)
    campo_dois = models.CharField(max_length=255, blank=True, null=True)
    campo_tres = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Item - Pedido Insight'
        verbose_name_plural = 'Itens - Pedido Insight'

    def __str__(self):
        return f'{self.pedido.numero} / {self.cod_produto} - {self.desc_produto}'

