from django.urls import path, include
from api.integration import *
from api.views import *
from rest_framework import routers


""" Rotas da API """
router = routers.DefaultRouter()
router.register('produto', ProdutoViewSet)
router.register('fornecedor', FornecedorViewSet)
router.register('estoque-atual', EstoqueAtualViewSet)
router.register('historico-estoque', HistEstoqueViewSet)
router.register('pedido-compra', PedidoViewSet)
router.register('ultima-entrada', UltEntradaViewSet)
router.register('venda', VendaViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('integration/fornecedor/', fornecedor_create, name='integration_fornecedor_create'),
    path('integration/produto/', produto_create, name='integration_produto_create'),
    path('integration/historico/', historico_create, name='integration_historico_create'),
    path('integration/venda/', venda_create, name='integration_venda_create'),
    path('integration/pedido/', pedido_create, name='integration_pedido_create'),
    path('integration/entrada/', entrada_create, name='integration_entrada_create'),
    path('integration/estoque/', estoque_create, name='integration_estoque_create'),
]