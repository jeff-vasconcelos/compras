from django.contrib import admin
from api.models import Produto

""" Adicionando dados da API de Produtos no Admin do DJANGO """
class Produtos(admin.ModelAdmin):
    list_display = ('cod_produto', 'desc_produto')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_per_page = 20

admin.site.register(Produto, Produtos)