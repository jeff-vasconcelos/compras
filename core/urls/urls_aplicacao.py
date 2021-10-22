from django.urls import path
from django.conf.urls.static import static
from core.export_files.generate_xls import export_xls
from core.views.usuario.usuario_views import *
from core.views.academy.academy_views import *
from core.views.home.home_views import *
from core.views.analise.analise_views import *
from core.views.alerta.alertas_views import *
from core.views.configuracao.configuracao_views import *
from core.export_files.generate_pdf import *
from core.views.pedido_insight.pedidos_views import *
from core.views.fornecedor.fornecedor_views import *
from core.views.utils.rotinas import teste


urlpatterns = [

    # REQUISIÇÕES AJAX
    path('search/prod', buscar_produto, name='results-produto'),
    path('search/fornec', buscar_fornecedor, name='results-fornecedor'),
    path('search/principio', buscar_pricipioativo, name='results-principio'),
    path('filter-fornec/', filtrar_produto_fornecedor, name='filter-fornecedor'),
    path('filter-prod/', filtrar_produto_produto, name='filter-produto'),
    path('filter-curva/', filtrar_produto_curva, name='filter-curva'),
    path('filter-marca/', filtrar_produto_marca, name='filter-marca'),
    path('filter-principio/', filtrar_produto_principio, name='filter-principio'),
    path('select-prod/', selecionar_produto, name='filter-produto'),

    path('home-graficos/', home_graficos, name='home_graficos'),

    # ALERTAS
    path('alertas/excesso/curva/<str:curva>', alerta_excesso_curva, name='alerta_excesso_curva'),
    path('alertas/excesso/filial/<int:filial>', alerta_excesso_filial, name='alerta_excesso_filial'),
    path('alertas/ruptura/curva/<str:curva>', alerta_ruptura_curva, name='alerta_ruptura_curva'),
    path('alertas/ruptura/filial/<int:filial>', alerta_ruptura_filial, name='alerta_ruptura_filial'),

    path('alertas/excesso/', alerta_all_excesso, name='alerta_all_excesso'),
    path('alertas/ruptura/', alerta_all_ruptura, name='alerta_all_ruptura'),

    # FORNECEDOR ALERTAS
    path('alertas/excesso/fornecedor/', excesso_fornecedor, name='alerta_excesso_fornecedor'),
    path('alertas/ruptura/fornecedor/', ruptura_fornecedor, name='alerta_ruptura_fornecedor'),
    path('alertas/excesso/fornecedor/<int:cod_fornecedor>/<int:filial>/', ver_excesso_fornecedor, name='ver_excesso_fornecedor'),
    path('alertas/ruptura/fornecedor/<int:cod_fornecedor>/<int:filial>/', ver_ruptura_fornecedor, name='ver_ruptura_fornecedor'),

    path('request/fornecedor/graf/', graficos_alert_fornec, name='request_fornec_graf'),


    # PEDIDOS
    path('add-produto-pedido/', add_prod_pedido_sessao, name='add-prod-pedido-sessao'),
    path('add-produtos-pedido-fornecedores/', add_pedido_sessao_fornecedores, name='add-produtos-pedido-fornecedores'),
    path('ver-produto-pedido/', ver_prod_pedido_sessao, name='ver-prod-pedido-sessao'),
    path('rm-produto-pedido/', rm_prod_pedido_sessao, name='rm-prod-pedido-sessao'),
    path('exportar-produto-pedido/', export_xls, name='exportar-pedido-sessao'),
    path('fornecedor-pedido/', pedido_save_db, name='fornecedor-pedido'),
    path('ver-pedido-pendentes/', pedidos_pedentes, name='ver-pedido-pendentes'),
    path('pedidos/ver/<int:pk>', ver_pedidos_insight, name='ver_pedidos_insight'),

    # PAGINAS
    path('home/', home_page, name='home_painel'),
    path('analise/', analise_painel, name='analise_painel'),
    # path('alertas/', alerta_painel, name='alertas_painel'),
    path('configuracoes/', configuracao_painel, name='configuracao_painel'),
    path('pedidos/', pedido_painel, name='pedido_painel'),

    # CONFIGURAÇÕES
    path('configuracoes/editar/fornecedor/<int:pk>', editar_fornecedor_conf, name='config_edit_forn'),
    path('configuracoes/editar/parametros/<int:pk>', editar_parametro_conf, name='config_edit_param'),
    path('configuracoes/adicionar/email/', adicionar_email_conf, name='config_add_email'),
    path('configuracoes/ver/email/', ver_emails_conf, name='config_ver_email'),
    path('configuracoes/remover/email/<int:pk>', remover_email_conf, name='config_remove_email'),
    path('configuracoes/editar/email/<int:pk>', editar_email_conf, name='config_editar_email'),
    path('configuracoes/email/', email_painel, name='email_painel'),
    path('configuracoes/fornecedores/', fornecedores_painel, name='fornecedores_painel'),

    # ACADEMY
    path('academy/', academy, name='academy'),
    path('academy/<slug>', video_academy, name='academy-video'),

    # USUÁRIOS
    path('cadastrar/usuario', cadastrar_usuario, name='cadastrar-usuario'),
    path('editar/perfil-usuario', editar_perfil, name='editar-perfil-usuario'),
    path('editar/usuario/<int:pk>', editar_usuario, name='editar-usuario'),
    path('listar/usuarios', lista_usuarios, name='listar-usuarios'),
    path('inativar/usuarios/<int:pk>', inativar_usuario, name='inativar-usuarios'),

    # PDFS
    path('pdf/pedidos/<int:pk>', pdf_pedidos_insight, name='pdf_pedidos_insight'),
    path('pdf/alertas/excesso/', pdf_excesso, name='pdf_excesso'),
    path('pdf/alertas/ruptura/', pdf_ruptura, name='pdf_ruptura'),


    # TODO rota de testes
    path('testando/', teste, name='testando'),
    path('teste/', pdf_pedidos_insight, name='get_all_logged_in_users'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
