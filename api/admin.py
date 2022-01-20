from django.contrib import admin
from api.models.estoque import Estoque
from api.models.fornecedor import Fornecedor
from api.models.historico import Historico
from api.models.pedido import Pedido
from api.models.produto import Produto
from api.models.entrada import Entrada
from api.models.venda import Venda

# from api.models.pedido_duplicado import PedidoDuplicado


""" Adicionando dados da API de Produtos no Admin do DJANGO """


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'desc_produto', 'fornecedor', 'empresa')
    list_display_links = ('cod_produto', 'desc_produto')
    search_fields = ('cod_produto', 'desc_produto',)
    list_filter = ('empresa',)
    list_per_page = 40


class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_fornecedor', 'desc_fornecedor', 'empresa')
    list_display_links = ('cod_fornecedor', 'desc_fornecedor',)
    search_fields = ('cod_fornecedor', 'desc_fornecedor',)
    list_filter = ('empresa',)
    list_per_page = 40


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'fornecedor', 'empresa', 'data')
    list_display_links = ('cod_produto', )
    search_fields = ('cod_produto', )
    list_filter = ('empresa',)
    list_per_page = 40


class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'fornecedor', 'empresa', 'data')
    list_display_links = ('cod_produto',)
    search_fields = ('cod_produto',)
    list_filter = ('empresa',)
    list_per_page = 40


class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'fornecedor', 'empresa', 'data')
    list_display_links = ('cod_produto',)
    search_fields = ('cod_produto', )
    list_filter = ('empresa',)
    list_per_page = 40


class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'fornecedor', 'empresa', 'data')
    list_display_links = ('cod_produto',)
    search_fields = ('cod_produto', )
    list_filter = ('empresa',)
    list_per_page = 40


class EntradaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_produto', 'fornecedor', 'empresa', 'data')
    list_display_links = ('cod_produto',)
    search_fields = ('cod_produto',)
    list_filter = ('empresa',)
    list_per_page = 40


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Estoque, EstoqueAdmin)
admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Historico, HistoricoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Venda, VendaAdmin)
# admin.site.register(PedidoDuplicado)
