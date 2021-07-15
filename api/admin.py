from django.contrib import admin
from api.models.estoque_atual_models import EstoqueAtual
from api.models.fornecedor_models import Fornecedor
from api.models.hist_estoque_models import HistEstoque
from api.models.p_compras_models import PedidoCompras
from api.models.produto_models import Produto
from api.models.ultima_entrada_models import UltimaEntrada
from api.models.vendas_models import Venda

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
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa')
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
admin.site.register(HistEstoque, Historico)
admin.site.register(PedidoCompras, Pedidos)
admin.site.register(UltimaEntrada, UltEntrada)
admin.site.register(Venda, Vendas)
