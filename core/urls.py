from django.urls import path
from core.views import *

urlpatterns = [
    path('painel/', index, name='index'),
]