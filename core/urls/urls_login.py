from django.urls import path
from django.contrib.auth import views as auth_views
from core.views.usuarios_views import *


urlpatterns = [
    path('login/', login_painel, name='login'),
    path('logout', logout_painel, name='logout'),


    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='aplicacao/login/reset_senha_email.html'),
         name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='aplicacao/login/reset_senha_mensagem.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='aplicacao/login/reset_senha.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='aplicacao/login/reset_senha_sucesso.html'),
         name='password_reset_complete'),

]
