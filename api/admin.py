from django.contrib import admin

from api.models.estoque_atual import EstoqueAtual
from api.models.fornecedor import Fornecedor
from api.models.historico_estoque import HistoricoEstoque
from api.models.pedido_compra import Pedido
from api.models.produto import Produto
from api.models.ultima_entrada import UltimaEntrada
from api.models.venda import Venda


""" Adicionando dados da API de Produtos no Admin do DJANGO """


class Produtos(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_filter = ('fornecedor', 'empresa',)
    list_per_page = 20


class Pedidos(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_filter = ('fornecedor', 'empresa',)
    list_per_page = 40


class Historico(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_filter = ('fornecedor', 'empresa',)
    list_per_page = 40


class Vendas(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa', 'data')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_filter = ('fornecedor', 'empresa',)
    list_per_page = 40


class Estoque(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_filter = ('fornecedor', 'empresa',)
    list_per_page = 40


class UltEntrada(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_filter = ('fornecedor', 'empresa',)
    list_per_page = 40


admin.site.register(Produto, Produtos)
admin.site.register(EstoqueAtual, Estoque)
admin.site.register(Fornecedor)
admin.site.register(HistoricoEstoque, Historico)
admin.site.register(Pedido, Pedidos)
admin.site.register(UltimaEntrada, UltEntrada)
admin.site.register(Venda, Vendas)
