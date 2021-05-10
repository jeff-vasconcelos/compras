from django.shortcuts import render


def home_painel(request, template_name='aplicacao/paginas/home.html'):
    return render(request, template_name)
