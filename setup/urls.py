import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('app-token-auth', views.obtain_auth_token, name='app-token-auth'),
    path('administracao/painel/', include('core.urls.urls_administracao')),
    path('painel/', include('core.urls.urls_aplicacao')),
    path('', include('core.urls.urls_login')),


    #TODO Remover rota debug_toolbar
    path('__debug__/', include(debug_toolbar.urls)),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Administração Insight'
admin.site.site_title = 'Ecluster'
admin.site.index_title = 'Insight Admin'

