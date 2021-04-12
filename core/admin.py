from django.contrib import admin
from core.models import *


class EnderecoInLine(admin.TabularInline):
    model = Endereco
    extra = 1


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_fantasia', 'cnpj')
    list_display_links = ('id', 'nome_fantasia')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj',)
    list_filter = ('ativo',)
    inlines = [
        EnderecoInLine,
    ]

admin.site.register(Endereco)
admin.site.register(Empresa, EmpresaAdmin)

