from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views.empresas_views import *


urlpatterns = [
    path('', index, name='index'),
    path('empresas/', listar_empresas, name='listar_empresas'),
    path('create/empresa', cadastrar_empresa, name='cadastrar_empresa'),
    path('detail/empresa/<int:pk>', detalhes_empresa, name='detalhes_empresa'),
    path('edit/empresa/<int:pk>', editar_empresa, name='editar_empresa'),
    path('active/empresa/<int:pk>', desativar_ativar_empresa, name='desativar_empresa'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)