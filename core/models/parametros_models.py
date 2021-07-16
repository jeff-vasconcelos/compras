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


class Email(models.Model):
    email = models.EmailField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='email_empresa',
                                blank=True, null=True)

    def __str__(self):
        return self.empresa.nome_fantasia