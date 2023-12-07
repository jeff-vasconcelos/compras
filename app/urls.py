from django.urls import path, include
from rest_framework import routers

from app.api.generic_views import (
    ProvidersCreate, ProductCreate, StockHistoryCreate,
    SalesCreate, OrdersCreate, EntryCreate, StockCreate
)
from app.api.health_check_view import health_check
from app.api.views import list_providers_by_company, list_products_by_company, list_branches_by_company, \
    list_orders_by_company, delete_orders_by_company, inactive_product_by_company
from app.api.viewsets import (
    ProviderViewSet, ProductViewSet, StockHistoryViewSet,
    SaleViewSet, OrderViewSet, EntryViewSet, CurrentStockViewSet
)

router = routers.DefaultRouter()
router.register('provider', ProviderViewSet)
router.register('product', ProductViewSet)
router.register('stock-history', StockHistoryViewSet)
router.register('product-sale', SaleViewSet)
router.register('order-buy', OrderViewSet)
router.register('product-entry', EntryViewSet)
router.register('stock-current', CurrentStockViewSet)

urlpatterns = [
    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),

    # STATUS ENDPOINT
    path('healthcheck/', health_check, name='health_check'),

    # INTEGRATION ENDPOINTS
    path('integration/provider/', ProvidersCreate.as_view(), name='provider_integration_create'),
    path('integration/product/', ProductCreate.as_view(), name='product_integration_create'),
    path('integration/stock-history/', StockHistoryCreate.as_view(), name='history_integration_create'),
    path('integration/product-sale/', SalesCreate.as_view(), name='sale_integration_create'),
    path('integration/order-buy/', OrdersCreate.as_view(), name='order_integration_create'),
    path('integration/product-entry/', EntryCreate.as_view(), name='entry_integration_create'),
    path('integration/stock-current/', StockCreate.as_view(), name='stock_integration_create'),

    # LIST ENDPOINTS BY COMPANY
    path('integration/providers/company/<str:pk>/', list_providers_by_company, name='orders_list_by_company'),
    path('integration/products/company/<str:pk>/', list_products_by_company, name='products_list_by_company'),
    path('integration/branches/company/<str:pk>/', list_branches_by_company, name='branches_list_by_company'),
    path('integration/orders/company/<str:pk>/', list_orders_by_company, name='orders_list_by_company'),

    # DELETE ENDPOINTS
    path('integration/delete/orders/<str:pk>/', delete_orders_by_company, name='orders_delete_by_company'),

    # INACTIVE ENDPOINTS
    path('integration/inactive/product/<str:pk>/', inactive_product_by_company, name='product_delete_by_company'),
]
