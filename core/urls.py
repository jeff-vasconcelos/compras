from django.urls import path
from core.views.empresas_views import *

urlpatterns = [
    path('', index, name='index'),
    path('teste/', teste, name='home'),
    path('empresas/', listar_empresas, name='listar_empresas'),
    path('create/empresa', cadastrar_empresa, name='cadastrar_empresa'),
    path('detail/empresa/<int:pk>', detalhes_empresa, name='detalhes_empresa'),
    path('edit/empresa/<int:pk>', editar_empresa, name='editar_empresa'),
    path('active/empresa/<int:pk>', desativar_ativar_empresa, name='desativar_empresa'),
]
