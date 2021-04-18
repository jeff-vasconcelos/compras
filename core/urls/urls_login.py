from django.urls import path
from core.views.usuarios_views import *

urlpatterns = [
    path('login/', login_painel, name='login'),
    path('logout', logout_painel, name='logout'),
]
