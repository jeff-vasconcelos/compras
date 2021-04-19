from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views.usuarios_views import *

urlpatterns = [
    path('home/', home_painel, name='home_painel'),

    path('cadastrar/usuario', cadastrar_usuario, name='cadastrar-usuario'),
    path('editar/perfil/usuario', editar_perfil, name='editar-perfil-usuario'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)