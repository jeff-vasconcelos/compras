from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from core.models.parametros_models import DadosEstoque, GraficoCurva, GraficoFaturamento
import locale
import pandas as pd

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# TODO (Status: Validando)
@login_required
def home_page(request, template_name='aplicacao/paginas/home.html'):
    """
        View responsável por renderiazar template de HOME
    """

    id_empresa = request.user.usuario.empresa_id
    dados_estoque = DadosEstoque.objects.filter(empresa__id=id_empresa)
    grafico_curva = GraficoCurva.objects.filter(empresa__id=id_empresa).order_by('curva')

    dados_df = pd.DataFrame(
        DadosEstoque.objects.filter(empresa__id=id_empresa).order_by('curva').values()
    )

    total_normal = dados_df['normal'].sum()
    total_parcial = dados_df['parcial'].sum()
    total_ruptura = dados_df['ruptura'].sum()
    total_excesso = dados_df['excesso'].sum()
    total_skus = dados_df['skus'].sum()

    totais_dados_estoque = {
        'total_normal': total_normal,
        'total_parcial': total_parcial,
        'total_ruptura': total_ruptura,
        'total_excesso': total_excesso,
        'total_skus': total_skus
    }

    # Gráfico Curva
    lista_grafico_curva = []
    for g in grafico_curva:
        disc_grafico = {
            'curva': g.curva,
            'normal': locale.currency(float(g.normal), grouping=True),
            'parcial': locale.currency(float(g.parcial), grouping=True),
            'excesso': locale.currency(float(g.excesso), grouping=True),
            'total': locale.currency(float(g.total), grouping=True)
        }
        lista_grafico_curva.append(disc_grafico)

    context = {
        'dados_estoque': dados_estoque,
        'totais_dados_estoque': totais_dados_estoque,
        'grafico_curva': lista_grafico_curva
    }

    return render(request, template_name, context)


# TODO (Status: Validando)
def home_graficos(request):
    """
        View responsável por enviar aos gráficos as respectivas informações
    """

    try:
        id_empresa = request.user.usuario.empresa_id
        grafico_um = GraficoCurva.objects.filter(empresa__id=id_empresa).order_by('curva')
        grafico_dois = GraficoFaturamento.objects.filter(empresa__id=id_empresa).order_by('curva')

        data = []

        # Gráfico curva
        porcent_curva = []

        for a in grafico_um:
            normal = float(a.normal)
            parcial = float(a.parcial)
            excesso = float(a.excesso)
            total = float(a.total)

            if normal != 0:
                part_normal = round(normal * 100 / total, 2)
            else:
                part_normal = 0

            if parcial != 0:
                part_parcial = round(parcial * 100 / total, 2)
            else:
                part_parcial = 0

            if excesso != 0:
                part_excesso = round(excesso * 100 / total, 2)
            else:
                part_excesso = 0

            curva_porc = {
                'curva': a.curva,
                'part_normal': part_normal,
                'part_parcial': part_parcial,
                'part_excesso': part_excesso
            }

            porcent_curva.append(curva_porc)

        # Gráfico faturamento
        curvas = []
        valores = []
        participacao = []

        for b in grafico_dois:
            curvas.append(b.curva)
            valores.append(b.total)
            participacao.append(b.participacao)

        curva_valor = {
            'curva': curvas,
            'valor': valores,
            'porcentagem': participacao
        }

        curva_faturamento = [curva_valor]

        # Enviando dados a requisição do ajax
        data.append(porcent_curva)
        data.append(curva_faturamento)

        return JsonResponse({'data': data})

    except Exception as error:
        data = [1, str(error)]

        return JsonResponse({'data': data})
