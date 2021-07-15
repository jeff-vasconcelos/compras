from django.shortcuts import render

from core.views.alertas_views import alertas


def home_painel(request, template_name='aplicacao/paginas/home.html'):
    return render(request, template_name)