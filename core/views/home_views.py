from chartjs.views.lines import BaseLineChartView
from django.http import JsonResponse
from django.shortcuts import render
from core.models.parametros_models import DadosEstoque, GraficoCurva, GraficoRuptura
from core.multifilial.pedidos import pedidos_compra
from core.multifilial.processa_produtos import a_multifiliais
from core.multifilial.ultima_entrada import ultima_entrada
from core.multifilial.vendas import vendas
from core.multifilial.curva_abc import abc
from core.multifilial.estoque_atual import estoque_atual


def home_painel(request, template_name='aplicacao/paginas/home.html'):
    dados_estoque = DadosEstoque.objects.filter(empresa__id=1)  # TODO automatizar empresa
    grafico_um = GraficoCurva.objects.filter(empresa__id=1)

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
        'totais_dados_estoque': totais_dados_estoque,
        'grafico_um': grafico_um
    }
    return render(request, template_name, contexto)


def testandoviews(request, template_name='testando_alerta.html'):
    # teste, teste2 = vendas(180, 1, 30)

    return render(request, template_name)


def DadosGrafico(request):
    id_empresa = request.user.usuario.empresa_id
    data = []
    if request.is_ajax():
        grafico_um = GraficoCurva.objects.filter(empresa__id=id_empresa)
        grafico_dois = GraficoRuptura.objects.filter(empresa__id=id_empresa)

        lista_um = []

        for um in grafico_um:
            graf_um = {
                'curva': um.curva,
                'normal': um.normal,
                'parcial': um.parcial,
                'excesso': um.excesso,
                'total': um.total,
            }
            lista_um.append(graf_um)


        return JsonResponse({'data': data})
    return JsonResponse({})
