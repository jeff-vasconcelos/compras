from django.shortcuts import render


def analise_painel(request, template_name='aplicacao/paginas/analise.html'):
    return render(request, template_name)
