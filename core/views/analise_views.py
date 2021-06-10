import csv
from math import ceil
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from api.models.fornecedor_models import *
from api.models.produto_models import *
import datetime

from core.models.empresas_models import Filial
from core.trata_dados.curva_abc import abc
from core.trata_dados.dados_produto import produto_dados
from core.trata_dados.datas import dia_semana_mes_ano
from core.trata_dados.estoque_atual import estoque_atual
from core.trata_dados.hist_estoque import historico_estoque
from core.trata_dados.infor_produto import dados_produto
from core.trata_dados.vendas import *
from core.trata_dados.avarias import *
from core.trata_dados.pedidos import *
from core.trata_dados.ultima_entrada import *
import pandas as pd


@login_required
def analise_painel(request, template_name='aplicacao/paginas/analise.html'):

    # teste = request.user.usuario.empresa_id
    # avar = produto_dados(182, teste, 120)
    # print("Dataframe avarias:", avar)
    return render(request, template_name)


def buscar_produto(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res = None
        produto = request.POST.get('produto')
        qs = Produto.objects.filter(
            Q(desc_produto__icontains=produto) |
            Q(cod_produto__icontains=produto),
            Q(empresa__id__exact=empresa)
        )
        if len(qs) > 0 and len(produto) > 0:
            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                    'emb': prod.embalagem
                }
                data.append(item)
            res = data
        else:
            res = "Nada encontrado!"
        return JsonResponse({'data': res})
    return JsonResponse({})


def buscar_fornecedor(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res_f = None
        fornecedor = request.POST.get('fornecedor')
        qs = Fornecedor.objects.filter(
            Q(desc_fornecedor__icontains=fornecedor) |
            Q(cod_fornecedor__icontains=fornecedor),
            Q(empresa__id__exact=empresa)
        )
        if len(qs) > 0 and len(fornecedor) > 0:
            data = []
            for fornec in qs:
                item = {
                    'pk': fornec.pk,
                    'nome': fornec.desc_fornecedor,
                    'cod': fornec.cod_fornecedor
                }
                data.append(item)
            res_f = data
        else:
            res_f = "Nada encontrado!"
        return JsonResponse({'data': res_f})
    return JsonResponse({})


def filtrar_produto_fornecedor(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res_fil_fornec = None
        fornecedor = request.POST.get('fornecedor')
        fornecedor = fornecedor.replace(",", "")

        lista_fornecedor = []
        for i in fornecedor:
            lista_fornecedor.append(int(i))

        qs = Produto.objects.filter(fornecedor_id__in=lista_fornecedor
                                    , empresa__id__exact=empresa).order_by('cod_produto')
        print(qs)

        if len(qs) > 0 and len(lista_fornecedor) > 0:
            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                    'emb': prod.embalagem
                }
                data.append(item)
            res_fil_fornec = data
        else:
            res_fil_fornec = "Nada encontrado!"
        return JsonResponse({'data': res_fil_fornec})
    return JsonResponse({})


def filtrar_produto_produto(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res_fil_prod = None
        produto = request.POST.get('produto')
        produto = produto.replace(",", "")

        lista_produto = []
        for i in produto:
            lista_produto.append(int(i))

        qs = Produto.objects.filter(id__in=lista_produto
                                    , empresa__id__exact=empresa).order_by('cod_produto')
        print(qs)

        if len(qs) > 0 and len(lista_produto) > 0:
            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                    'emb': prod.embalagem
                }
                data.append(item)
            res_fil_prod = data
        else:
            res_fil_prod = "Nada encontrado!"
        return JsonResponse({'data': res_fil_prod})
    return JsonResponse({})


def selecionar_produto(request):
    empresa = request.user.usuario.empresa_id

    if request.is_ajax():
        info_prod = None
        produto = request.POST.get('produto')
        leadtime = int(request.POST.get('leadtime'))
        t_reposicao = int(request.POST.get('tempo_reposicao'))

        qs = Produto.objects.get(id=produto, empresa__id=empresa)

        produto_codigo = qs.cod_produto
        fornecedor_codigo = qs.cod_fornecedor

        produto_dados, pedidos_todos = dados_produto(produto_codigo, fornecedor_codigo, empresa, leadtime, t_reposicao)

        if produto_dados is None:
            messages.error(request, "O produto selecionado pode não ter vendas no periodo!")

            return JsonResponse({'data': 0})

        else:
            dt_entrada = produto_dados['dt_ult_ent'][0]
            if dt_entrada == '-':
                dt_u_entrada = dt_entrada
            else:
                dt_u_entrada = dt_entrada.strftime('%d/%m/%Y')

            rupt = -1
            sugestao = float(produto_dados['sugestao'])
            qt_un_caixa = float(produto_dados['qt_unit_caixa'])

            sug_cx = sugestao / qt_un_caixa
            sug_cx = ceil(sug_cx)
            sug_unit = sug_cx * qt_un_caixa

            data = []
            itens_analise = {
                'filial': int(produto_dados['cod_filial']),
                'estoque': int(produto_dados['estoque_dispon']),
                'avaria': int(produto_dados['avarias']),
                'saldo': int(produto_dados['saldo']),
                'dt_ult_entrada': dt_u_entrada,
                'qt_ult_entrada': int(produto_dados['qt_ult_ent']),
                'vl_ult_entrada': float(produto_dados['vl_ult_ent']),
                'dde': float(produto_dados['dde']),
                'est_seguranca': float(produto_dados['estoque_segur']),
                'p_reposicao': float(produto_dados['ponto_repo']),
                'sugestao': float(produto_dados['sugestao']),
                'sugestao_caixa': sug_cx,
                'sugestao_unidade': sug_unit,
                'curva': str(produto_dados['curva'][0]),
                'media_ajustada': str(produto_dados['media_ajustada'][0]),
                'ruptura': float(produto_dados['ruptura']),
                'ruptura_porc': float(produto_dados['ruptura_porc']),
                'condicao_estoque': str(produto_dados['condicao_estoque'][0]),
            }
            itens_pedido = []
            for index, row in pedidos_todos.iterrows():
                itens = {
                    'p_cod_filial': int(row['cod_filial']),
                    'p_cod_produto': int(row['cod_produto']),
                    'p_desc_produto': str(row['desc_produto']),
                    'p_saldo': int(row['saldo']),
                    'p_data': str(row['data'].strftime('%d/%m/%Y')),
                }

                itens_pedido.append(itens)
            print(itens_pedido)

            mapa = mapas_serie(empresa, produto)

            data.append(itens_analise) #0
            data.append(mapa) #1
            #data.append(itens_pedido) #2

            return JsonResponse({'data': data})

    return JsonResponse({})


def mapas_serie(empresa, produto):
    info_prod = None
    qs = Produto.objects.get(id=produto, empresa__id=empresa)
    produto_codigo = qs.cod_produto

    parametros = Parametro.objects.get(empresa_id=empresa)
    df_vendas, info_produto = vendas(produto_codigo, empresa, parametros.periodo)

    datas = dia_semana_mes_ano(empresa)
    df_historico = historico_estoque(produto_codigo, empresa, parametros.periodo)
    df_historico['data'] = pd.to_datetime(df_historico['data'], format='%Y-%m-%d')
    hist_estoque = pd.merge(datas, df_historico, how="left", on=["data"])
    hist_estoque['qt_estoque'].fillna(0, inplace=True)
    hist_estoque = hist_estoque.sort_values(by=['data'], ascending=True)

    data_day_est = hist_estoque['data'].copy()
    data_dia_est = data_day_est.dt.strftime('%d/%m/%Y')
    hist_estoque['data_serie_hist_est'] = hist_estoque['semana'].str.cat(data_dia_est, sep=" - ")


    print('hist_estoque')
    print(hist_estoque)

    df_vendas = df_vendas.sort_values(by=['data'], ascending=True)
    data_day = df_vendas['data'].copy()
    data_dia = data_day.dt.strftime('%d/%m/%Y')

    df_vendas['data_serie_hist'] = df_vendas['semana'].str.cat(data_dia, sep=" - ")

    # print(df_vendas)

    data_max = list(df_vendas['max'])
    data_med = list(df_vendas['media'])
    data_min = list(df_vendas['min'])
    data_preco = list(df_vendas['preco_unit'])
    data_custo = list(df_vendas['custo_fin'])
    data_lucro = list(df_vendas['lucro'])
    data_qtvenda = list(df_vendas['qt_vendas'])
    label_dt_serie = list(df_vendas['data_serie_hist'])

    qt_estoque = list(hist_estoque['qt_estoque'])
    label_dt_serie_est = list(hist_estoque['data_serie_hist_est'])

    graf_prod = []
    item = {
        'data_max': data_max,
        'data_med': data_med,
        'data_min': data_min,
        'data_preco': data_preco,
        'data_custo': data_custo,
        'data_lucro': data_lucro,
        'data_qtvenda': data_qtvenda,
        'label_dt_serie': label_dt_serie,
        'qt_estoque': qt_estoque,
        'label_dt_serie_est': label_dt_serie_est
    }

    return item


def add_prod_pedido_sessao(request):
    if request.is_ajax():
        produto_id = request.POST.get('produto')
        #TODO Aumatizar filial
        cod_filial = 1

        qt_digitada = request.POST.get('qt_digitada')
        pr_compra = request.POST.get('pr_compra')
        margem = request.POST.get('margem')
        pr_sugerido = request.POST.get('pr_sugerido')
        dde = request.POST.get('dde')

        prod_qs = Produto.objects.get(id=produto_id)
        produto_nome = prod_qs.desc_produto
        produto_codigo = prod_qs.cod_produto

        if not request.session.get('pedido_produto'):
            request.session['pedido_produto'] = {}
            request.session.save()

        pedido = request.session['pedido_produto']

        pedido[produto_id] = {
            'ped_produto_id': produto_id,
            'ped_produto_cod': produto_codigo,
            'ped_produto_nome': produto_nome,
            'ped_cod_filial': cod_filial,
            'ped_qt_digitada': qt_digitada,
            'ped_pr_compra': pr_compra,
            'ped_margem': margem,
            'ped_pr_sugerido': pr_sugerido,
            'ped_dde': dde,
        }

        request.session.save()
        print(request.session['pedido_produto'])

        messages.success(request, "Produto adicionado com sucesso!")
        return JsonResponse({'data': produto_id})


def ver_prod_pedido_sessao(request):
    if request.is_ajax():
        contexto = request.session.get('pedido_produto', [])
        lista = []
        for value in contexto.values():
            temp = value
            lista.append(temp)

        return JsonResponse({'data': lista})


def rm_prod_pedido_sessao(request):
    if request.is_ajax():
        produto_id = request.POST.get('produto')

        del request.session['pedido_produto'][produto_id]
        request.session.save()

        return JsonResponse({'data': 0})


def export_csv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['cod_produto', 'preco', 'quantidade'])

    pedido = request.session.get('pedido_produto', [])
    lista = []

    for value in pedido.values():
        temp = value
        print(temp)
        for valor in temp.values():
            t = valor
            print
            lista.append(t)
            writer.writerow(lista)

    print(lista)


    response['Content-Disposition'] = 'attachment; filename="pedido_insight.csv"'

    return response