from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

""" Rotas da API """
router = routers.DefaultRouter()
router.register('produto', ProdutoViewSet)
router.register('fornecedor', FornecedorViewSet)
router.register('avaria', AvariaViewSet)
router.register('estoque-atual', EstoqueAtualViewSet)
router.register('historico-estoque', HistEstoqueViewSet)
router.register('pedido-compra', PedidoViewSet)
router.register('ultima-entrada', UltEntradaViewSet)
router.register('venda', VendaViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth', views.obtain_auth_token, name='api-token-auth'),
    path('administracao/painel/', include('core.urls.urls_administracao')),
    path('painel/', include('core.urls.urls_aplicacao')),
    path('acesso/', include('core.urls.urls_login')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Administração Insight'
admin.site.site_title = 'Ecluster'
admin.site.index_title = 'Insight Admin'