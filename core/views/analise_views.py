from math import ceil
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from api.models.produto import *
from core.alertas.verificador import verifica_produto
from core.multifilial.processa_produtos import processa_produtos_filiais
from core.multifilial.curva_abc import abc
from core.trata_dados.curva_abc import abc
from core.trata_dados.historico_estoque import historico_estoque
from core.trata_dados.vendas import *
from core.trata_dados.pedidos import *
from core.models.empresas_models import Filial
import csv
import pandas as pd


@login_required
def analise_painel(request, template_name='aplicacao/paginas/analise.html'):
    empresa = request.user.usuario.empresa_id
    filiais = Filial.objects.filter(empresa__id__exact=empresa)
    context = {
        'filiais': filiais
    }
    return render(request, template_name, context)


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
        fornecedor = fornecedor.replace(",", " ")

        a = fornecedor.split()
        b = []

        for elemento in a:
            b.append(int(elemento))

        lista_fornecedor = []
        for i in b:
            lista_fornecedor.append(int(i))

        qs = Produto.objects.filter(fornecedor_id__in=lista_fornecedor, empresa__id__exact=empresa).order_by('cod_produto')

        if len(qs) > 0 and len(lista_fornecedor) > 0:
            marcas = []
            marcas_itens = []

            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                    'emb': prod.embalagem,
                }
                if prod.marca not in marcas:
                    marcas.append(prod.marca)
                data.append(item)

            for i in marcas:
                itens_marcas = {
                    'marca_p': i
                }
                marcas_itens.append(itens_marcas)

            res_fil_fornec = []
            res_fil_fornec.append(data)
            res_fil_fornec.append(marcas_itens)
        else:
            res_fil_fornec = "Nada encontrado!"
        return JsonResponse({'data': res_fil_fornec})
    return JsonResponse({})


def filtrar_produto_produto(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res_fil_prod = None
        produto = request.POST.get('produto')
        produto = produto.replace(",", " ")
        a = produto.split()
        b = []
        for elemento in a:
            b.append(int(elemento))

        lista_produto = []
        for i in b:
            lista_produto.append(int(i))

        qs = Produto.objects.filter(id__in=lista_produto, empresa__id__exact=empresa).order_by('cod_produto')

        if len(qs) > 0 and len(lista_produto) > 0:
            marcas = []
            marcas_itens = []

            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                    'emb': prod.embalagem,
                }
                if prod.marca not in marcas:
                    marcas.append(prod.marca)
                data.append(item)

            for i in marcas:
                itens_marcas = {
                    'marca_p': i
                }
                marcas_itens.append(itens_marcas)

            res_fil_prod = []
            res_fil_prod.append(data)
            res_fil_prod.append(marcas_itens)
        else:
            res_fil_prod = "Nada encontrado!"
        return JsonResponse({'data': res_fil_prod})
    return JsonResponse({})


def filtrar_produto_curva(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res_fil_curva = None
        id_fornecedor = request.POST.get('fornecedor')
        id_produto = request.POST.get('produto')

        curva = request.POST.get('curva')

        parametros = Parametro.objects.get(empresa_id=empresa)
        if curva == '0':
            return JsonResponse({})
        else:

            if id_fornecedor is not None and id_fornecedor != '':
                fornecedor = id_fornecedor.replace(",", " ")

                a = fornecedor.split()
                b = []

                for elemento in a:
                    b.append(int(elemento))

                lista_fornecedor = []
                for i in b:
                    lista_fornecedor.append(int(i))

                fornec = Fornecedor.objects.filter(id__in=lista_fornecedor)

                list_fornec = []
                for i in fornec:
                    cod_fornec = i.cod_fornecedor
                    list_fornec.append(cod_fornec)

                curva_f = abc(list_fornec, empresa, parametros.periodo)
                curva_f = curva_f.query('curva== @curva')

                if not curva_f.empty:
                    codprod = curva_f['cod_produto']
                    list_produto = []
                    for items in codprod.iteritems():
                        list_produto.append(int(items[1]))

                    qs = Produto.objects.filter(cod_produto__in=list_produto, empresa__id__exact=empresa).order_by(
                        'cod_produto')

                    if len(qs) > 0 and len(list_produto) > 0:
                        data = []
                        for prod in qs:
                            item = {
                                'pk': prod.pk,
                                'nome': prod.desc_produto,
                                'cod': prod.cod_produto,
                                'emb': prod.embalagem
                            }
                            data.append(item)
                        res_fil_curva = data
                    else:
                        res_fil_curva = "Nada encontrado!"
                    return JsonResponse({'data': res_fil_curva})
                else:
                    res = "FALSE"
                    return JsonResponse({'data': res})

            if id_produto is not None and id_produto != '':

                produt = id_produto.replace(",", " ")

                a = produt.split()
                b = []

                for elemento in a:
                    b.append(int(elemento))

                lista_produto = []
                for i in b:
                    lista_produto.append(int(i))

                prod = Produto.objects.filter(id__in=lista_produto)

                list_fornec = []
                for i in prod:
                    cod_fornec = i.fornecedor.cod_fornecedor
                    list_fornec.append(cod_fornec)

                curva_f = abc(list_fornec, empresa, parametros.periodo)
                curva_f = curva_f.query('curva== @curva')

                if not curva_f.empty:
                    codprod = curva_f['cod_produto']
                    list_produto = []
                    for items in codprod.iteritems():
                        if items[0] in lista_produto:
                            list_produto.append(int(items[1]))

                    qs = Produto.objects.filter(cod_produto__in=list_produto, empresa__id__exact=empresa).order_by(
                        'cod_produto')

                    if len(qs) > 0 and len(list_produto) > 0:
                        data = []
                        for prod in qs:
                            item = {
                                'pk': prod.pk,
                                'nome': prod.desc_produto,
                                'cod': prod.cod_produto,
                                'emb': prod.embalagem
                            }
                            data.append(item)
                        res_fil_curva = data
                    else:
                        res = "FALSE"
                        return JsonResponse({'data': res})
                    return JsonResponse({'data': res_fil_curva})
                else:
                    res = "FALSE"
                    return JsonResponse({'data': res})

    return JsonResponse({})


def filtrar_produto_marca(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res_fil_curva = None
        marca = request.POST.get('marca')

        fornecedor = request.POST.get('fornecedor')
        fornecedor = fornecedor.replace(",", " ")

        a = fornecedor.split()
        b = []

        for elemento in a:
            b.append(int(elemento))

        lista_fornecedor = []
        for i in b:
            lista_fornecedor.append(int(i))

        qs = Produto.objects.filter(marca=marca, fornecedor_id__in=lista_fornecedor, empresa__id__exact=empresa).order_by('cod_produto')

        if len(qs) > 0:
            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                    'emb': prod.embalagem,
                }
                data.append(item)
            res_fil_curva = data
        else:
            res_fil_curva = "Nada encontrado!"
        return JsonResponse({'data': res_fil_curva})
    return JsonResponse({})


def selecionar_produto(request):
    global info_prod_filiais
    id_empresa = request.user.usuario.empresa_id

    if request.is_ajax():
        id_produto = int(request.POST.get('produto'))
        leadtime = int(request.POST.get('leadtime'))
        t_reposicao = int(request.POST.get('tempo_reposicao'))
        filialselecionada = int(request.POST.get('filial'))

        qs = Produto.objects.get(id=id_produto, empresa__id=id_empresa)

        parametros = Parametro.objects.get(empresa_id=id_empresa)

        verif_produto = verifica_produto(qs.cod_produto, id_empresa, parametros.periodo)

        if verif_produto == True:

            infor_produtos_filiais = processa_produtos_filiais(id_produto, id_empresa, leadtime, t_reposicao, filialselecionada)

            df_filial_selecionada = infor_produtos_filiais.query('filial == @filialselecionada')
            df_filial_selecionada = df_filial_selecionada.drop(columns=[
                'filial','estoque', 'avaria', 'saldo', 'dt_ult_entrada', 'qt_ult_entrada', 'vl_ult_entrada', 'dde',
                'est_seguranca', 'p_reposicao', 'sugestao', 'sugestao_caixa', 'sugestao_unidade', 'preco_tabela', 'margem'
            ])

            item_filial_selecionada = df_filial_selecionada.to_dict('records')

            for i in item_filial_selecionada:
                info_prod_filiais = i

            infor_produtos_filiais = infor_produtos_filiais.drop(columns=[
                'curva', 'media_ajustada', 'ruptura_porc', 'ruptura_cor', 'condicao_estoque', 'porc_media', 'media_simples'
            ])
            infor_produtos_filiais = infor_produtos_filiais.to_dict('records')


            data = []

            mapa = mapas_serie(id_empresa, id_produto, filialselecionada)

            data.append(infor_produtos_filiais)  # 0
            data.append(mapa)  # 1
            data.append(info_prod_filiais) #2

            return JsonResponse({'data': data})

        else:
            return JsonResponse({'data': 0})

    return JsonResponse({})


def mapas_serie(empresa, produto, cod_filial):
    info_prod = None
    qs = Produto.objects.get(id=produto, empresa__id=empresa)
    produto_codigo = qs.cod_produto

    parametros = Parametro.objects.get(empresa_id=empresa)
    df_vendas, info_produto = vendas(produto_codigo, empresa, parametros.periodo, cod_filial)

    datas = dia_semana_mes_ano(empresa)
    df_historico = historico_estoque(produto_codigo, empresa, parametros.periodo)
    df_historico['data'] = pd.to_datetime(df_historico['data'], format='%Y-%m-%d')
    hist_estoque = pd.merge(datas, df_historico, how="left", on=["data"])
    hist_estoque['qt_estoque'].fillna(0, inplace=True)
    hist_estoque = hist_estoque.sort_values(by=['data'], ascending=True)

    data_day_est = hist_estoque['data'].copy()
    data_dia_est = data_day_est.dt.strftime('%d/%m/%Y')
    hist_estoque['data_serie_hist_est'] = hist_estoque['semana'].str.cat(data_dia_est, sep=" - ")


    df_vendas = df_vendas.sort_values(by=['data'], ascending=True)
    data_day = df_vendas['data'].copy()
    data_dia = data_day.dt.strftime('%d/%m/%Y')

    df_vendas['data_serie_hist'] = df_vendas['semana'].str.cat(data_dia, sep=" - ")

    data_max = list(df_vendas['max'])
    data_med = list(df_vendas['media'])
    data_min = list(df_vendas['min'])
    data_preco = list(df_vendas['preco_unit'])
    data_custo = list(df_vendas['custo_fin'])
    data_lucro = list(df_vendas['lucro'])
    data_qtvenda = list((df_vendas['qt_vendas']))
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
        if produto_id != "0":
            # TODO Aumatizar filial
            cod_filial = 1

            qt_digitada = request.POST.get('qt_digitada')
            pr_compra = request.POST.get('pr_compra')

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
                'ped_pr_compra': pr_compra,
                'ped_qt_digitada': qt_digitada,
            }

            request.session.save()

            res = "SUCESSO"
            return JsonResponse({'data': res})
        else:
            res = "FALHOU"
            return JsonResponse({'data': res})


def ver_prod_pedido_sessao(request):
    if request.is_ajax():
        contexto = request.session.get('pedido_produto', [])
        lista = []

        if not contexto:
            res = "FALSE"
            return JsonResponse({'data': res})

        else:
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

        del [temp['ped_cod_filial']]
        del [temp['ped_produto_nome']]
        del [temp['ped_produto_id']]

        lista.append(temp)

    for i in lista:
        writer.writerow(i.values())

    response['Content-Disposition'] = 'attachment; filename="importar_pedido.csv"'

    return response


def pedidos_pedentes(request):
    empresa = request.user.usuario.empresa_id
    filial = 1

    if request.is_ajax():
        produto_id = request.POST.get('produto')

        if produto_id == "0":
            res = "FALSE"
            return JsonResponse({'data': res})

        else:
            prod_qs = Produto.objects.get(id=produto_id)
            produto_codigo = prod_qs.cod_produto

            p, pedidos = pedidos_compras(produto_codigo, empresa, filial)

            pedidos['data'] = pd.to_datetime(pedidos.data).dt.strftime('%d/%m/%Y')
            pedidos.rename(columns={'data': 'data_ped'}, inplace=True)

            pedidos['data_ped'] = pedidos['data_ped'].astype(str)

            pedid = pedidos.assign(**pedidos.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict(
                "records")

            return JsonResponse({'data': pedid})
    return JsonResponse({})
