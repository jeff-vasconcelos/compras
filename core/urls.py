from django.urls import path
from core.views.empresas_views import *

urlpatterns = [
    path('painel/', index, name='index'),
    path('painel/empresa', listar_empresas, name='listar_empresas'),
]
