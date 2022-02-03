from django.urls import path, include
from api.integration import *
from api.views import *
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views


""" API routes """
router = routers.DefaultRouter()

router.register('providers', ProviderViewSet)
router.register('products', ProductViewSet)
router.register('stock-histories', StockHistoryViewSet)
router.register('product-sales', SaleViewSet)
router.register('buy-orders', OrderBuyViewSet)
router.register('entry-products', EntryViewSet)
router.register('stock-current', StockCurrentViewSet)


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # ENDPOINT DE STATUS DA API
    path('integration/', access_valid, name='access_valid'),

    # ENDPOINTS PARA CRIAR REGISTROS NO BANCO DE DADOS NA ETAPA DE INTEGRACAO AGENDADA
    path('', include(router.urls)),

    # ENDPOINTS PARA CRIAR REGISTROS NO BANCO DE DADOS NA ETAPA DE INTEGRACAO
    path('integration/providers/', ProvidersCreate.as_view(), name='providers_integration_create'),
    path('integration/products/', ProductCreate.as_view(), name='products_integration_create'),
    path('integration/stock-histories/', StockHistoryCreate.as_view(), name='histories_integration_create'),
    path('integration/product-sales/', SalesCreate.as_view(), name='sales_integration_create'),
    path('integration/buy-orders/', OrdersCreate.as_view(), name='orders_integration_create'),
    path('integration/entry-products/', EntryCreate.as_view(), name='entry_integration_create'),
    path('integration/stock-current/', StockCreate.as_view(), name='stock_integration_create'),

    # ENDPOINTS PARA LISTAR: FORNECEDORES, PRODUTOS, FILIAIS, PEDIDOS E REMOVER PEDIDO POR EMPRESA (EMPRESA_ID)
    path('integration/providers-company/<str:pk>/', list_providers_by_company, name='orders_list_by_company'),
    path('integration/products-company/<str:pk>/', list_products_by_company, name='products_list_by_company'),
    path('integration/branches-company/<str:pk>/', list_branches_by_company, name='branches_list_by_company'),
    path('integration/orders-company/<str:pk>/', list_orders_by_company, name='orders_list_by_company'),
    path('integration/orders-company/delete/<str:pk>/', delete_duplicate_orders_by_company, name='orders_delete_by_company'),

    path('integration/stock-company/<str:pk>/', list_stock_by_company, name='stock_by_company'),
]