from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views.usuario_views import *
from core.views.academy_views import *
from core.views.home_views import *
from core.views.analise_views import *


urlpatterns = [
    path('search/prod', buscar_produto, name='results-produto'),
    path('search/fornec', buscar_fornecedor, name='results-fornecedor'),
    path('filter-fornec/', filtrar_produto_fornecedor, name='filter-fornecedor'),
    path('filter-prod/', filtrar_produto_produto, name='filter-produto'),
    path('filter-curva/', filtrar_produto_curva, name='filter-curva'),
    path('filter-marca/', filtrar_produto_marca, name='filter-marca'),
    path('select-prod/', selecionar_produto, name='filter-produto'),
    # TODO remover path de url
    path('graficos-prod-selec/', export_csv, name='graficos-prod-selec'),

    #path('ver-pedido-pendente/', ver_pedido_pendente, name='ver-pedido-pendente'),

    path('add-produto-pedido/', add_prod_pedido_sessao, name='add-prod-pedido-sessao'),
    path('ver-produto-pedido/', ver_prod_pedido_sessao, name='ver-prod-pedido-sessao'),
    path('rm-produto-pedido/', rm_prod_pedido_sessao, name='rm-prod-pedido-sessao'),
    path('exportar-produto-pedido/', export_csv, name='exportar-pedido-sessao'),

    path('ver-pedido-pendentes/', pedidos_pedentes, name='ver-pedido-pendentes'),


    path('home/', home_painel, name='home_painel'),
    path('analise/', analise_painel, name='analise_painel'),

    path('academy/', academy, name='academy'),
    path('academy/<slug>', video_academy, name='academy-video'),

    path('cadastrar/usuario', cadastrar_usuario, name='cadastrar-usuario'),
    path('editar/perfil-usuario', editar_perfil, name='editar-perfil-usuario'),
    path('editar/usuario/<int:pk>', editar_usuario, name='editar-usuario'),
    path('listar/usuarios', lista_usuarios, name='listar-usuarios'),
    path('inativar/usuarios/<int:pk>', inativar_usuario, name='inativar-usuarios'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)