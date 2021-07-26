from chartjs.views.lines import BaseLineChartView
from django.shortcuts import render
from core.models.parametros_models import DadosEstoque, GraficoCurva
from core.multifilial.pedidos import pedidos_compra
from core.multifilial.processa_produtos import a_multifiliais
from core.multifilial.ultima_entrada import ultima_entrada
from core.multifilial.vendas import vendas
from core.multifilial.curva_abc import abc
from core.multifilial.estoque_atual import estoque_atual


def home_painel(request, template_name='aplicacao/paginas/home.html'):
    dados_estoque = DadosEstoque.objects.filter(empresa__id=1) #TODO automatizar empresa
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
        'grafico_um':grafico_um
    }
    return render(request, template_name, contexto)


def testandoviews(request, template_name='testando_alerta.html'):
    # teste, teste2 = vendas(180, 1, 30)
    # teste = abc([16], 1, 30)
    # teste = estoque_atual(180, 1)
    # teste = pedidos_compra(180, 1)
    # teste = ultima_entrada(180, 1, 30)
    # teste = a_multifiliais(180, 16, 1, 15, 30, 30, [1, 2])
    # print(teste)
    return render(request, template_name)

class DadosGrafico(BaseLineChartView):
    def get_data(self):
        dados = [
            10,
            30,
            40,
            50
        ]
        return dados
    def get_labels(self):
        labels = [
            "um",
            "dois",
            "tres",
            "quatro"
        ]