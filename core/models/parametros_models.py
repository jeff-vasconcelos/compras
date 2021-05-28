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
    curva_x = models.FloatField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='parametros',
                                blank=True, null=True)

