from django.contrib import admin
from api.models.produto_models import Produto
from api.models.fornecedor_models import Fornecedor

""" Adicionando dados da API de Produtos no Admin do DJANGO """


class Produtos(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_per_page = 20


admin.site.register(Produto, Produtos)
admin.site.register(Fornecedor)