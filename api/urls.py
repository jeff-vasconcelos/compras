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
    path('integration/', access_valid, name='access_valid'),

    path('integration/fornecedor/', FornecedorCreate.as_view(), name='integration_fornecedor_create'),
    path('integration/produto/', ProdutoCreate.as_view(), name='integration_produto_create'),

    path('integration/fornecedor/empresa/<str:pk>/', listar_fornecedor_empresa, name='listar_fornecedor_empresa'),
    path('integration/produto/empresa/<str:pk>/', listar_produtos_empresa, name='listar_produtos_empresa'),
    path('integration/filial/empresa/<str:pk>/', listar_filiais_empresa, name='listar_filial_empresa'),

    path('integration/historico/', HistoricoCreate.as_view(), name='integration_historico_create'),
    path('integration/venda/', VendaCreate.as_view(), name='integration_venda_create'),
    path('integration/pedido/', PedidoCreate.as_view(), name='integration_pedido_create'),
    path('integration/entrada/', EntradaCreate.as_view(), name='integration_entrada_create'),
    path('integration/estoque/', EstoqueCreate.as_view(), name='integration_estoque_create'),

]