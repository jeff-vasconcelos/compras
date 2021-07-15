from django.db import models
from django.contrib.auth.models import User
from core.models.empresas_models import Empresa
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("imagens_usuarios", filename)


""" Modelo de usuário relacionado a empresas """
class Usuario(models.Model):
    TIPO = (
        ('Administrador', 'Administrador'),
        ('Comprador', 'Comprador')
    )
    tipo = models.CharField(max_length=15, null=False, blank=False, choices=TIPO, verbose_name='Tipo')
    imagem = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='usuario')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='empresa')

    def __str__(self):
        return self.usuario.username
