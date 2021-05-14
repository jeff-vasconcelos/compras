from django.db import models
from core.models.empresas_models import Empresa


""" Modelo de parametros """
class Parametro(models.Model):
    meta_compras = models.IntegerField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='parametros',
                                blank=True, null=True)

    def __str__(self):
        return self.meta_compras