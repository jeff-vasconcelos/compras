from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views.usuarios_views import *
from core.views.academy_views import *


urlpatterns = [
    path('home/', home_painel, name='home_painel'),

    path('academy/', academy, name='academy'),
    path('academy/<slug>', video_academy, name='academy-video'),

    path('cadastrar/usuario', cadastrar_usuario, name='cadastrar-usuario'),
    path('editar/perfil-usuario', editar_perfil, name='editar-perfil-usuario'),
    path('editar/usuario/<int:pk>', editar_usuario, name='editar-usuario'),
    path('listar/usuarios', lista_usuarios, name='listar-usuarios'),
    path('inativar/usuarios/<int:pk>', inativar_usuario, name='inativar-usuarios'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)