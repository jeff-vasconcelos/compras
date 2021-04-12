from django.db import models
from django.contrib.auth.models import User
from core.models import Empresa


""" Modelo de permissões de usuarios """
class Permissao(models.Model):
    meta = models.BooleanField(default=False, verbose_name='Permitir cadastrar/alterar metas')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='usuario_permissao')

    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'

    def __str__(self):
        return self.usuario.username


""" Modelo de usuário relacionado a empresas """
class Usuario(models.Model):
    TIPO = (
        ('admin', 'Administrador'),
        ('comp', 'Comprador')
    )
    tipo = models.CharField(max_length=15, null=True, blank=True, choices=TIPO, verbose_name='Tipo')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='usuario')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='empresa')

    def __str__(self):
        return self.usuario.username
