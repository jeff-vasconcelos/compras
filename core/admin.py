from django.contrib import admin
from core.models.empresas_models import *
from core.models.parametros_models import *
from core.models.usuarios_models import *
from core.models.academy_models import *

admin.site.register(Empresa)
admin.site.register(Filial)
admin.site.register(Usuario)
admin.site.register(Academy)
admin.site.register(Parametro)

