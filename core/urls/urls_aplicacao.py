from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views.usuario_views import *
from core.views.academy_views import *
from core.views.home_views import *
from core.views.analise_views import *
from core.views.alertas_views import *
from core.views.configuracao_views import *


from core.multifilial.processa_produtos import a_multifiliais

urlpatterns = [
    path('search/prod', buscar_produto, name='results-produto'),
    path('search/fornec', buscar_fornecedor, name='results-fornecedor'),
    path('search/principio', buscar_pricipioativo, name='results-principio'),
    path('filter-fornec/', filtrar_produto_fornecedor, name='filter-fornecedor'),
    path('filter-prod/', filtrar_produto_produto, name='filter-produto'),
    path('filter-curva/', filtrar_produto_curva, name='filter-curva'),
    path('filter-marca/', filtrar_produto_marca, name='filter-marca'),
    path('filter-principio/', filtrar_produto_principio, name='filter-principio'),
    path('select-prod/', selecionar_produto, name='filter-produto'),

    path('alertas/curva/<str:curva>', alerta_por_curva, name='filter-filial-curva'),
    path('alertas/condicao/<str:condicao>', alerta_por_condicao, name='filter-filial-condicao'),
    path('alertas/filial/<int:filial>', alerta_por_filial, name='filter-filial-alerta'),

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
    path('alertas/', alerta_painel, name='alertas_painel'),
    path('configuracoes/', configuracao_painel, name='configuracao_painel'),

    path('configuracoes/editar/fornecedor/<int:pk>', editar_fornecedor_conf, name='config_edit_forn'),
    path('configuracoes/editar/parametros/<int:pk>', editar_parametro_conf, name='config_edit_param'),

    path('configuracoes/adicionar/email/', adicionar_email_conf, name='config_add_email'),
    path('configuracoes/ver/email/', ver_emails_conf, name='config_ver_email'),
    path('configuracoes/remover/email/<int:pk>', remover_email_conf, name='config_remove_email'),
    path('configuracoes/editar/email/<int:pk>', editar_email_conf, name='config_editar_email'),


    path('academy/', academy, name='academy'),
    path('academy/<slug>', video_academy, name='academy-video'),

    path('cadastrar/usuario', cadastrar_usuario, name='cadastrar-usuario'),
    path('editar/perfil-usuario', editar_perfil, name='editar-perfil-usuario'),
    path('editar/usuario/<int:pk>', editar_usuario, name='editar-usuario'),
    path('listar/usuarios', lista_usuarios, name='listar-usuarios'),
    path('inativar/usuarios/<int:pk>', inativar_usuario, name='inativar-usuarios'),

    #TODO rota de testes
    path('testando/', teste, name='testando'),
    path('teste/', get_all_logged_in_users, name='get_all_logged_in_users'),

    #path('graficos_home', DadosGrafico, name='graficos_home')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)