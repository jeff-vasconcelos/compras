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


class AlertaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'cod_filial', 'empresa')
    list_display_links = ('cod_produto',)
    search_fields = ('cod_produto', )
    list_filter = ('empresa',)
    list_per_page = 40


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa')
    list_display_links = ('id', 'empresa',)
    search_fields = ('empresa',)
    list_filter = ('empresa',)
    list_per_page = 40


class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa')
    list_display_links = ('id', 'empresa',)
    search_fields = ('empresa',)
    list_filter = ('empresa',)
    list_per_page = 40


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedidoInsight
    extra = 1


class PedidoInsAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa', 'usuario', 'created_at')
    list_display_links = ('id', 'empresa',)
    search_fields = ('empresa',)
    list_filter = ('empresa',)
    list_per_page = 40
    inlines = [
        ItemPedidoInline
    ]


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Filial, FilialAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Academy)
admin.site.register(Parametro, ConfigAdmin)
admin.site.register(PedidoInsight, PedidoInsAdmin)
admin.site.register(ItemPedidoInsight)
admin.site.register(Alerta, AlertaAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(DadosEstoque)
admin.site.register(GraficoCurva)
admin.site.register(GraficoFaturamento)

