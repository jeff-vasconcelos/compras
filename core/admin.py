from django.contrib import admin
from core.models.empresas_models import *
from core.models.parametros_models import *
from core.models.usuarios_models import *
from core.models.academy_models import *
from core.models.pedidos_models import *


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_fantasia', 'razao_social', 'cnpj', 'estado')
    list_display_links = ('nome_fantasia',)
    search_fields = ('nome_fantasia',)
    list_filter = ('principio_ativo',)
    list_per_page = 40


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'tipo', 'empresa')
    list_display_links = ('usuario',)
    search_fields = ('usuario', 'empresa',)
    list_filter = ('empresa',)
    list_per_page = 40


class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'desc_filial', 'empresa')
    list_display_links = ('desc_filial',)
    search_fields = ('desc_filial', 'empresa',)
    list_filter = ('empresa',)
    list_per_page = 40


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Filial, FilialAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Academy)
admin.site.register(Parametro)
admin.site.register(PedidoInsight)
admin.site.register(Alerta)
admin.site.register(Email)
admin.site.register(DadosEstoque)
admin.site.register(GraficoCurva)
admin.site.register(GraficoRuptura)

