from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from core.models.parametros_models import DadosEstoque, GraficoCurva, GraficoRuptura
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


@login_required
def home_painel(request, template_name='aplicacao/paginas/home.html'):

    id_empresa = request.user.usuario.empresa_id
    dados_estoque = DadosEstoque.objects.filter(empresa__id=id_empresa)
    grafico_um = GraficoCurva.objects.filter(empresa__id=id_empresa).order_by('curva')

    # DADOS DE ESTOQUE
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


    #GRAFICO UM
    g_um = []
    for g in grafico_um:

        f_normal = float(g.normal)
        f_parcial = float(g.parcial)
        f_excesso = float(g.excesso)
        f_total = float(g.total)

        dic_garfico = {
            'curva': g.curva,
            'normal': locale.currency(f_normal, grouping=True),
            'parcial': locale.currency(f_parcial, grouping=True),
            'excesso': locale.currency(f_excesso, grouping=True),
            'total': locale.currency(f_total, grouping=True)
        }
        g_um.append(dic_garfico)

    contexto = {
        'dadosestoque': dados_estoque,
        'totais_dados_estoque': totais_dados_estoque,
        'grafico_um': g_um
    }
    return render(request, template_name, contexto)


def home_graficos(request):
    id_empresa = request.user.usuario.empresa_id
    grafico_um = GraficoCurva.objects.filter(empresa__id=id_empresa)
    grafico_dois = GraficoRuptura.objects.filter(empresa__id=id_empresa)

    data = []

    # GRAFICO UM
    porcent_curva = []

    for a in grafico_um:
        normal = float(a.normal)
        parcial = float(a.parcial)
        excesso = float(a.excesso)
        total = float(a.total)

        if normal != 0:
            p_normal = round(normal * 100 / total, 2)
        else:
            p_normal = 0

        if parcial != 0:
            p_parcial = round(parcial * 100 / total, 2)
        else:
            p_parcial = 0

        if excesso != 0:
            p_excesso = round(excesso * 100 / total, 2)
        else:
            p_excesso = 0

        curva_porc = {
            'curva': a.curva,
            'p_normal': p_normal,
            'p_parcial': p_parcial,
            'p_excesso': p_excesso
        }

        porcent_curva.append(curva_porc)

    # GRAFICO DOIS
    valor_curva_ruptura = []
    curvas = []
    valores = []

    for b in grafico_dois:
        curvas.append(b.curva)
        valores.append(b.total)

    curva_valor = {
        'curva': curvas,
        'valor': valores
    }

    valor_curva_ruptura.append(curva_valor)

    # LISTA COM TODOS OS DADOS
    data.append(porcent_curva)
    data.append(valor_curva_ruptura)

    return JsonResponse({'data': data})