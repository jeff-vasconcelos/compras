from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views.empresa_views import *


urlpatterns = [
    path('', index, name='index'),

    # EMPRESAS
    path('empresas/', listar_empresas, name='listar_empresas'),
    path('empresa/cadastrar/', cadastrar_empresa, name='cadastrar_empresa'),
    path('empresa/detalhes/<int:pk>', detalhes_empresa, name='detalhes_empresa'),
    path('empresa/editar/<int:pk>', editar_empresa, name='editar_empresa'),
    path('empresa/active/<int:pk>', desativar_ativar_empresa, name='desativar_empresa'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)