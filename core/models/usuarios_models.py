from django.db import models
from django.contrib.auth.models import User
from core.models.empresas_models import Empresa
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("imagens_usuarios", filename)

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
    imagem = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='usuario')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='empresa')

    def __str__(self):
        return self.usuario.username
