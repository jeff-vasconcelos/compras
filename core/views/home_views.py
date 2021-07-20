from django.shortcuts import render

from core.alertas.processa_produtos_alertas import *
from core.models.parametros_models import DadosEstoque
from core.alertas.vendas_alertas import vendas

from core.views.alertas_views import alertas


def home_painel(request, template_name='aplicacao/paginas/home.html'):
    dados_estoque = DadosEstoque.objects.filter(empresa__id=1)

    t_skus = 0
    t_normal = 0
    t_parcial = 0
    t_ruptura = 0
    t_excesso = 0

    for dados in dados_estoque:
        t_skus = t_skus + dados.skus
        t_normal = t_normal + dados.normal
        t_parcial = t_parcial + dados.parcial
        t_ruptura = t_ruptura + dados.ruptura
        t_excesso = t_excesso + dados.excesso


    totais_dados_estoque = {
        't_skus': t_skus,
        't_normal': t_normal,
        't_parcial': t_parcial,
        't_ruptura': t_ruptura,
        't_excesso': t_excesso
    }

    contexto = {
        'dadosestoque': dados_estoque,
        'totais_dados_estoque': totais_dados_estoque
    }
    return render(request, template_name, contexto)


def testandoviews(request, template_name='testando_alerta.html'):
    # resultado = vendas(180, 1, 30)
    # dados_produto(180, 16, 1, 15, 30, 30)
    # processa_produtos_filiais(180, 16, 1, 15, 30, 30)
    resultado = processa_produtos_filiais(180, 16, 1, 15, 30, 30)

    # print(resultado)
    return render(request, template_name)