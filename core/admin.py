from django.contrib import admin
from core.models.empresas_models import *
from core.models.usuarios_models import *

admin.site.register(Empresa)
admin.site.register(Usuario)

