from django.db import models
from core.models.empresas_models import Empresa


""" Modelo de parametros """
class Parametro(models.Model):
    periodo = models.IntegerField(null=True, blank=True)
    curva_a = models.FloatField(null=True, blank=True)
    curva_b = models.FloatField(null=True, blank=True)
    curva_c = models.FloatField(null=True, blank=True)
    curva_d = models.FloatField(null=True, blank=True)
    curva_e = models.FloatField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='parametros',
                                blank=True, null=True)

    # campo_um = models.CharField(max_length=255, null=True, blank=True)
    # campo_dois = models.CharField(max_length=255, null=True, blank=True)
    # campo_tres = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Configuração Empresa'
        verbose_name_plural = 'Configurações Empresas'

    def __str__(self):
        return self.empresa.nome_fantasia


class Email(models.Model):
    email = models.EmailField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='email_empresa',
                                blank=True, null=True)

    def __str__(self):
        return self.empresa.nome_fantasia


class DadosEstoque(models.Model):
    curva = models.CharField(max_length=255, blank=True, null=True)
    skus = models.IntegerField(null=True, blank=True)
    normal = models.IntegerField(null=True, blank=True)
    parcial = models.IntegerField(null=True, blank=True)
    ruptura = models.IntegerField(null=True, blank=True)
    excesso = models.IntegerField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='dadosestoque_empresa',
                                blank=True, null=True)

    class Meta:
        verbose_name = 'Home - Dados Estoque'
        verbose_name_plural = 'Home - Dados Estoque'

    def __str__(self):
        return self.empresa.nome_fantasia


class GraficoCurva(models.Model):
    curva = models.CharField(max_length=255, blank=True, null=True)
    normal = models.CharField(max_length=255, null=True, blank=True)
    parcial = models.CharField(max_length=255, null=True, blank=True)
    excesso = models.CharField(max_length=255, null=True, blank=True)
    total = models.CharField(max_length=255, null=True, blank=True)

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='grafcurva_empresa',
                                blank=True, null=True)

    class Meta:
        verbose_name = 'Home - Grafico Um'
        verbose_name_plural = 'Home - Grafico Um'

    def __str__(self):
        return self.empresa.nome_fantasia


class GraficoFaturamento(models.Model):
    curva = models.CharField(max_length=255, blank=True, null=True)
    total = models.FloatField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='grafruptura_empresa',
                                blank=True, null=True)
    participacao = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'Home - Grafico Dois'
        verbose_name_plural = 'Home - Grafico Dois'

    def __str__(self):
        return self.empresa.nome_fantasia
