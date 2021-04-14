from django.urls import path
from core.views.empresas_views import *

urlpatterns = [
    path('', index, name='index'),
    path('empresas/', listar_empresas, name='listar_empresas'),
    path('create/empresa', cadastrar_empresa, name='cadastrar_empresa'),
    path('detail/empresa/<int:pk>', detalhes_empresa, name='detalhes_empresa'),
]
