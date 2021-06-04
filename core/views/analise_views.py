from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from api.models.fornecedor_models import *
from api.models.produto_models import *
import datetime
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

        produto_dados = dados_produto(produto_codigo, fornecedor_codigo, empresa, leadtime, t_reposicao)

        if produto_dados is None:
            print("O produto não pode ser analisado! O produto pode não ter vendas.")
            print(produto_dados)

            data = []
            item = {
                'filial': '',
                'estoque': '',
                'avaria': '',
                'saldo': '',
                'dt_ult_entrada': '',
                'qt_ult_entrada': '',
                'vl_ult_entrada': '',
                'est_seguranca': '',
                'p_reposicao': '',
                'cx_fech': '',
                'cx': '',
                'unidade': '',
                'preco_tab': '',
                'margem': '',
                'curva': '',
                'media_ajustada': '',
            }
            data.append(item)
            info_prod = data

            return JsonResponse({'data': info_prod})

        else:
            print(produto_dados)
            dt_entrada = produto_dados['dt_ult_ent'][0]
            if dt_entrada == '-':
                dt_u_entrada = dt_entrada
            else:
                dt_u_entrada = dt_entrada.strftime('%d/%m/%Y')

            rupt = -1

            data = []
            item = {
                'filial': int(produto_dados['cod_filial']),
                'estoque': int(produto_dados['estoque_dispon']),
                'avaria': int(produto_dados['avarias']),
                'saldo': int(produto_dados['saldo']),
                'dt_ult_entrada': dt_u_entrada,
                'qt_ult_entrada': int(produto_dados['qt_ult_ent']),
                'vl_ult_entrada': float(produto_dados['vl_ult_ent']),
                'est_seguranca': float(produto_dados['estoque_segur']),
                'p_reposicao': float(produto_dados['ponto_repo']),

                'sugestao': float(produto_dados['sugestao']),

                # 'cx_fech': int(produto_dados['vl_ult_ent']),
                # 'cx': int(produto_dados['vl_ult_ent']),
                # 'unidade': float(produto_dados['vl_ult_ent']),
                # 'preco_tab': float(produto_dados['vl_ult_ent']),
                # 'margem': float(produto_dados['vl_ult_ent']),
                'curva': str(produto_dados['curva'][0]),
                'media_ajustada': str(produto_dados['media_ajustada'][0]),
                'ruptura': rupt
            }
            data.append(item)
            info_prod = data

            return JsonResponse({'data': info_prod})

    return JsonResponse({})


def mapas_serie(request):
    empresa = request.user.usuario.empresa_id

    if request.is_ajax():
        info_prod = None
        produto = request.POST.get('produto')
        print(produto, "produto para o grafico")
        qs = Produto.objects.get(id=produto, empresa__id=empresa)
        produto_codigo = qs.cod_produto

        parametros = Parametro.objects.get(empresa_id=empresa)
        df_vendas, info_produto = vendas(produto_codigo, empresa, parametros.periodo)

        data_day = df_vendas['data'].copy()
        data_dia = data_day.dt.strftime('%d/%m/%Y')

        df_vendas['data_serie_hist'] = df_vendas['semana'].str.cat(data_dia, sep=" - ")

        print(df_vendas)

        data_max = list(df_vendas['max'])
        data_med = list(df_vendas['media'])
        data_min = list(df_vendas['min'])
        data_preco = list(df_vendas['preco_unit'])
        data_custo = list(df_vendas['custo_fin'])
        data_lucro = list(df_vendas['lucro'])
        data_qtvenda = list(df_vendas['qt_vendas'])
        label_dt_serie = list(df_vendas['data_serie_hist'])

        graf_prod = []
        item = {
            'data_max': data_max,
            'data_med': data_med,
            'data_min': data_min,
            'data_preco': data_preco,
            'data_custo': data_custo,
            'data_lucro': data_lucro,
            'data_qtvenda': data_qtvenda,
            'label_dt_serie': label_dt_serie
        }

        graf_prod.append(item)
        return JsonResponse({'data': item})

    return JsonResponse({})


