import datetime
from math import ceil
import xlwt
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from api.models.produto import *
from api.models.venda import Venda
from core.alertas.verificador import verifica_produto
from core.models.parametros_models import Parametro
from core.multifilial.processa_produtos import a_multifiliais
from core.multifilial.curva_abc import abc
from core.trata_dados.curva_abc import curva_abc
from core.trata_dados.datas import dia_semana_mes_ano
from core.multifilial.historico_estoque import historico_estoque
from core.trata_dados.pedidos import pedidos_todos
from core.models.empresas_models import Filial
import csv
import pandas as pd
from core.multifilial.vendas import vendas
from core.models.pedidos_models import *
import re  # pacote com as rotinas de expressão regular
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


@login_required
def analise_painel(request, template_name='aplicacao/paginas/analise.html'):
    id_empresa = request.user.usuario.empresa_id
    empresa = Empresa.objects.get(id=id_empresa)

    if empresa.principio_ativo == True:
        p_ativo = True

    else:
        p_ativo = False

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)
    context = {
        'filiais': filiais,
        'p_ativo': p_ativo
    }
    return render(request, template_name, context)


def buscar_produto(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res = None
        produto = request.POST.get('produto')

        pattern_int = re.compile(r"(0|-?[1-9][0-9]*)")

        if pattern_int.match(produto):
            qs = Produto.objects.filter(
                Q(cod_produto__icontains=produto),
                Q(empresa__id__exact=empresa)
            )[:15]

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

        else:
            if len(produto) >= 3:
                qs = Produto.objects.filter(
                    Q(desc_produto__icontains=produto),
                    Q(empresa__id__exact=empresa)
                )[:15]

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

            else:
                res = "Continue digitando!"
            return JsonResponse({'data': res})

    return JsonResponse({})


def buscar_fornecedor(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res_f = None
        fornecedor = request.POST.get('fornecedor')

        pattern_int = re.compile(r"(0|-?[1-9][0-9]*)")

        if pattern_int.match(fornecedor):
            qs = Fornecedor.objects.filter(
                Q(cod_fornecedor__icontains=fornecedor),
                Q(empresa__id__exact=empresa)
            )[:15]

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

        else:
            if len(fornecedor) >= 3:

                qs = Fornecedor.objects.filter(
                    Q(desc_fornecedor__icontains=fornecedor),
                    Q(empresa__id__exact=empresa)
                )[:15]

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

            else:
                res = "Continue digitando!"
            return JsonResponse({'data': res})

    return JsonResponse({})


def buscar_pricipioativo(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        res = None
        produto = request.POST.get('princ')

        if len(produto) >= 3:
            qs = Produto.objects.filter(
                Q(principio_ativo__icontains=produto),
                Q(empresa__id__exact=empresa)
            )[:15]

            if len(qs) > 0 and len(produto) > 0:
                data = []
                principios = []
                for prod in qs:
                    if prod.principio_ativo not in principios:
                        principios.append(prod.principio_ativo)

                for i in principios:
                    item = {
                        'principio': i,
                    }

                    data.append(item)
                res = data
            else:
                res = "Nada encontrado!"
            return JsonResponse({'data': res})

        else:
            res = "Continue digitando!"
        return JsonResponse({'data': res})

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

        qs = Produto.objects.filter(fornecedor_id__in=lista_fornecedor, empresa__id__exact=empresa).order_by(
            'desc_produto')

        if len(qs) > 0 and len(lista_fornecedor) > 0:
            marcas = []
            marcas_itens = []

            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                }
                if prod.marca not in marcas and prod.marca is not None:
                    marcas.append(prod.marca)
                data.append(item)

            for i in marcas:
                itens_marcas = {
                    'marca_p': i,
                    'marca_p_desc': i
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

        qs = Produto.objects.filter(id__in=lista_produto, empresa__id__exact=empresa).order_by('desc_produto')

        if len(qs) > 0 and len(lista_produto) > 0:
            marcas = []
            marcas_itens = []

            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                }
                if prod.marca not in marcas and prod.marca is not None:
                    marcas.append(prod.marca)
                data.append(item)

            for i in marcas:
                itens_marcas = {
                    'marca_p': i,
                    'marca_p_desc': i
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
    id_empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        id_fornecedor = request.POST.get('fornecedor')
        id_produto = request.POST.get('produto')
        principio = request.POST.get('principio')

        curva = request.POST.get('curva')
        marca = request.POST.get('marca')

        parametros = Parametro.objects.get(empresa_id=id_empresa)

        if curva == '0':
            return JsonResponse({})

        else:

            if marca != '0':

                # BUSCANDO POR FORNECEDOR
                if id_fornecedor is not None and id_fornecedor != '':
                    fornecedor = id_fornecedor.replace(",", " ")

                    a = fornecedor.split()
                    b = []

                    for elemento in a:
                        b.append(int(elemento))

                    lista_fornecedor = []
                    for i in b:
                        lista_fornecedor.append(int(i))

                    fornec = Fornecedor.objects.filter(
                        id__in=lista_fornecedor,
                        empresa__id__exact=id_empresa
                    )

                    list_fornec = []
                    for i in fornec:
                        cod_fornec = i.cod_fornecedor
                        list_fornec.append(cod_fornec)

                    curva_f = curva_abc(list_fornec, id_empresa, parametros.periodo)
                    # (cod_fornecedor, id_empresa, periodo, lista_filiais)
                    curva_f = curva_f.query('curva== @curva')

                    if not curva_f.empty:
                        codprod = curva_f['cod_produto']
                        list_produto = []
                        for items in codprod.iteritems():
                            list_produto.append(int(items[1]))

                        qs = Produto.objects.filter(
                            cod_produto__in=list_produto,
                            empresa__id__exact=id_empresa,
                            marca=marca
                        ).order_by('desc_produto')

                        if len(qs) > 0 and len(list_produto) > 0:
                            data = []
                            for prod in qs:
                                item = {
                                    'pk': prod.pk,
                                    'nome': prod.desc_produto,
                                    'cod': prod.cod_produto,
                                }
                                data.append(item)
                            res_fil_curva = data
                        else:
                            res_fil_curva = "Nada encontrado!"
                        return JsonResponse({'data': res_fil_curva})
                    else:
                        res = "FALSE"
                        return JsonResponse({'data': res})

                # BUSCANDO POR PRODUTO
                if id_produto is not None and id_produto != '':

                    produt = id_produto.replace(",", " ")

                    a = produt.split()
                    b = []

                    for elemento in a:
                        b.append(int(elemento))

                    lista_produto = []
                    for i in b:
                        lista_produto.append(int(i))

                    prod = Produto.objects.filter(
                        id__in=lista_produto,
                        empresa__id__exact=id_empresa
                    )

                    list_fornec = []
                    for i in prod:
                        cod_fornec = i.fornecedor.cod_fornecedor
                        list_fornec.append(cod_fornec)

                    curva_f = curva_abc(list_fornec, id_empresa, parametros.periodo)
                    curva_f = curva_f.query('curva== @curva')

                    if not curva_f.empty:
                        codprod = curva_f['cod_produto']
                        list_produto = []
                        for items in codprod.iteritems():
                            if items[0] in lista_produto:
                                list_produto.append(int(items[1]))

                        qs = Produto.objects.filter(
                            cod_produto__in=list_produto,
                            empresa__id__exact=id_empresa,
                            marca=marca
                        ).order_by('desc_produto')

                        if len(qs) > 0 and len(list_produto) > 0:
                            data = []
                            for prod in qs:
                                item = {
                                    'pk': prod.pk,
                                    'nome': prod.desc_produto,
                                    'cod': prod.cod_produto,
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

                # BUSCANDO POR PRICIPIO
                if principio is not None and principio != '':
                    p_ativo = principio.replace(",", " ")

                    a = p_ativo.split()
                    p = []

                    for elemento in a:
                        p.append(elemento)

                    lista_p_ativo = []
                    for i in p:
                        lista_p_ativo.append(i)

                    prod = Produto.objects.filter(
                        principio_ativo__in=lista_p_ativo,
                        empresa__id__exact=id_empresa
                    )

                    list_fornec = []
                    for i in prod:
                        cod_fornec = i.cod_fornecedor
                        list_fornec.append(cod_fornec)

                    curva_f = curva_abc(list_fornec, id_empresa, parametros.periodo)

                    curva_f = curva_f.query('curva== @curva')

                    if not curva_f.empty:
                        codprod = curva_f['cod_produto']
                        list_produto = []
                        for items in codprod.iteritems():
                            list_produto.append(int(items[1]))

                        qs = Produto.objects.filter(
                            cod_produto__in=list_produto,
                            empresa__id__exact=id_empresa,
                            marca=marca
                        ).order_by('desc_produto')

                        if len(qs) > 0 and len(list_produto) > 0:
                            data = []
                            for prod in qs:
                                item = {
                                    'pk': prod.pk,
                                    'nome': prod.desc_produto,
                                    'cod': prod.cod_produto,
                                }
                                data.append(item)
                            res_fil_curva = data
                        else:
                            res_fil_curva = "Nada encontrado!"
                        return JsonResponse({'data': res_fil_curva})
                    else:
                        res = "FALSE"
                        return JsonResponse({'data': res})

            else:
                # BUSCA POR FORNECEDOR
                if id_fornecedor is not None and id_fornecedor != '':
                    fornecedor = id_fornecedor.replace(",", " ")

                    a = fornecedor.split()
                    b = []

                    for elemento in a:
                        b.append(int(elemento))

                    lista_fornecedor = []
                    for i in b:
                        lista_fornecedor.append(int(i))

                    fornec = Fornecedor.objects.filter(
                        id__in=lista_fornecedor,
                        empresa__id__exact=id_empresa
                    )

                    list_fornec = []
                    for i in fornec:
                        cod_fornec = i.cod_fornecedor
                        list_fornec.append(cod_fornec)

                    curva_f = curva_abc(list_fornec, id_empresa, parametros.periodo)
                    # (cod_fornecedor, id_empresa, periodo, lista_filiais)
                    curva_f = curva_f.query('curva== @curva')

                    if not curva_f.empty:
                        codprod = curva_f['cod_produto']
                        list_produto = []
                        for items in codprod.iteritems():
                            list_produto.append(int(items[1]))

                        qs = Produto.objects.filter(
                            cod_produto__in=list_produto,
                            empresa__id__exact=id_empresa
                        ).order_by('desc_produto')

                        if len(qs) > 0 and len(list_produto) > 0:
                            data = []
                            for prod in qs:
                                item = {
                                    'pk': prod.pk,
                                    'nome': prod.desc_produto,
                                    'cod': prod.cod_produto,
                                }
                                data.append(item)
                            res_fil_curva = data
                        else:
                            res_fil_curva = "Nada encontrado!"
                        return JsonResponse({'data': res_fil_curva})
                    else:
                        res = "FALSE"
                        return JsonResponse({'data': res})

                # BUSCA POR PRODUTO
                if id_produto is not None and id_produto != '':

                    produt = id_produto.replace(",", " ")

                    a = produt.split()
                    b = []

                    for elemento in a:
                        b.append(int(elemento))

                    lista_produto = []
                    for i in b:
                        lista_produto.append(int(i))

                    prod = Produto.objects.filter(
                        id__in=lista_produto,
                        empresa__id__exact=id_empresa
                    )

                    list_fornec = []
                    for i in prod:
                        cod_fornec = i.fornecedor.cod_fornecedor
                        list_fornec.append(cod_fornec)

                    curva_f = curva_abc(list_fornec, id_empresa, parametros.periodo)
                    curva_f = curva_f.query('curva== @curva')

                    if not curva_f.empty:
                        codprod = curva_f['cod_produto']
                        list_produto = []
                        for items in codprod.iteritems():
                            if items[0] in lista_produto:
                                list_produto.append(int(items[1]))

                        qs = Produto.objects.filter(
                            cod_produto__in=list_produto,
                            empresa__id__exact=id_empresa
                        ).order_by('desc_produto')

                        if len(qs) > 0 and len(list_produto) > 0:
                            data = []
                            for prod in qs:
                                item = {
                                    'pk': prod.pk,
                                    'nome': prod.desc_produto,
                                    'cod': prod.cod_produto,
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

                # BUSCANDO POR PRICIPIO
                if principio is not None and principio != '':
                    p_ativo = principio.replace(",", " ")

                    a = p_ativo.split()
                    p = []

                    for elemento in a:
                        p.append(elemento)

                    lista_p_ativo = []
                    for i in p:
                        lista_p_ativo.append(i)

                    prod = Produto.objects.filter(
                        principio_ativo__in=lista_p_ativo,
                        empresa__id__exact=id_empresa
                    )

                    list_fornec = []
                    for i in prod:
                        cod_fornec = i.cod_fornecedor
                        list_fornec.append(cod_fornec)

                    curva_f = curva_abc(list_fornec, id_empresa, parametros.periodo)

                    curva_f = curva_f.query('curva== @curva')

                    if not curva_f.empty:
                        codprod = curva_f['cod_produto']
                        list_produto = []
                        for items in codprod.iteritems():
                            list_produto.append(int(items[1]))

                        qs = Produto.objects.filter(
                            cod_produto__in=list_produto,
                            empresa__id__exact=id_empresa
                        ).order_by('desc_produto')

                        if len(qs) > 0 and len(list_produto) > 0:
                            data = []
                            for prod in qs:
                                item = {
                                    'pk': prod.pk,
                                    'nome': prod.desc_produto,
                                    'cod': prod.cod_produto,
                                }
                                data.append(item)
                            res_fil_curva = data
                        else:
                            res_fil_curva = "Nada encontrado!"
                        return JsonResponse({'data': res_fil_curva})
                    else:
                        res = "FALSE"
                        return JsonResponse({'data': res})

    return JsonResponse({})


def filtrar_produto_marca(request):
    id_empresa = request.user.usuario.empresa_id
    # parametros = Parametro.objects.get(empresa_id=id_empresa)
    if request.is_ajax():
        marca = request.POST.get('marca')
        fornecedor = request.POST.get('fornecedor')
        produto = request.POST.get('produto')
        p_ativo = request.POST.get('principio')
        # curva = request.POST.get('curva')

        if fornecedor != '':
            fornecedor = fornecedor.replace(",", " ")

            a = fornecedor.split()
            b = []

            for elemento in a:
                b.append(int(elemento))

            lista_fornecedor = []
            for i in b:
                lista_fornecedor.append(int(i))

            qs = Produto.objects.filter(
                marca=marca,
                fornecedor_id__in=lista_fornecedor,
                empresa__id__exact=id_empresa
            ).order_by('desc_produto')

            if len(qs) > 0:
                data = []
                for prod in qs:
                    item = {
                        'pk': prod.pk,
                        'nome': prod.desc_produto,
                        'cod': prod.cod_produto,
                    }
                    data.append(item)
                res_fil_curva = data
            else:
                res_fil_curva = "Nada encontrado!"
            return JsonResponse({'data': res_fil_curva})

        if produto != '':
            produto = produto.replace(",", " ")

            a = produto.split()
            b = []

            for elemento in a:
                b.append(int(elemento))

            lista_produto = []
            for i in b:
                lista_produto.append(int(i))

            qs = Produto.objects.filter(
                marca=marca,
                id__in=lista_produto,
                empresa__id__exact=id_empresa
            ).order_by('desc_produto')

            if len(qs) > 0:
                data = []
                for prod in qs:
                    item = {
                        'pk': prod.pk,
                        'nome': prod.desc_produto,
                        'cod': prod.cod_produto,
                    }
                    data.append(item)
                res_fil_curva = data
            else:
                res_fil_curva = "Nada encontrado!"
            return JsonResponse({'data': res_fil_curva})

        if p_ativo != '':
            principio_ativo = p_ativo.split(",")

            qs = Produto.objects.filter(
                marca=marca,
                principio_ativo__in=principio_ativo,
                empresa__id__exact=id_empresa
            ).order_by('desc_produto')

            if len(qs) > 0:
                data = []
                for prod in qs:
                    item = {
                        'pk': prod.pk,
                        'nome': prod.desc_produto,
                        'cod': prod.cod_produto,
                    }
                    data.append(item)
                res_fil_curva = data
            else:
                res_fil_curva = "Nada encontrado!"
            return JsonResponse({'data': res_fil_curva})
    return JsonResponse({})


def filtrar_produto_principio(request):
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        p_ativo = request.POST.get('principio')
        principio_ativo = p_ativo.split(",")

        qs = Produto.objects.filter(
            principio_ativo__in=principio_ativo,
            empresa__id__exact=empresa
        ).order_by('desc_produto')

        if len(qs) > 0 and len(principio_ativo) > 0:
            marcas = []
            marcas_itens = []

            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                }
                if prod.marca not in marcas and prod.marca is not None:
                    marcas.append(prod.marca)
                data.append(item)

            for i in marcas:
                itens_marcas = {
                    'marca_p': i,
                    'marca_p_desc': i
                }
                marcas_itens.append(itens_marcas)

            res_fil_prod = []
            res_fil_prod.append(data)
            res_fil_prod.append(marcas_itens)
        else:
            res_fil_prod = "Nada encontrado!"
        return JsonResponse({'data': res_fil_prod})
    return JsonResponse({})


def selecionar_produto(request) -> object:
    global info_prod_filiais
    id_empresa = request.user.usuario.empresa_id

    if request.is_ajax():
        try:

            # DADOS DA REQUISIÇÃO
            id_produto = int(request.POST.get('produto'))
            leadtime = int(request.POST.get('leadtime'))
            t_reposicao = int(request.POST.get('tempo_reposicao'))
            filial_selecionada = int(request.POST.get('filial'))

            # VERIFICANDO SE HOUVE VENDAS NO PERIODO INDEPENDE DA FILIAL
            qs = Produto.objects.get(
                id=id_produto,
                empresa__id=id_empresa
            )

            parametros = Parametro.objects.get(
                empresa_id=id_empresa
            )
            verif_produto = verifica_produto(qs.cod_produto, id_empresa, parametros.periodo)
            lista_filiais = []

            cod_produto = qs.cod_produto
            cod_fornecedor = qs.cod_fornecedor
            periodo = parametros.periodo

            if verif_produto == True:

                # VERIFCANDO FILIAIS COM VENDAS DO PRODUTO
                se_vendas = Venda.objects.filter(
                    empresa__id__exact=id_empresa,
                    produto__id__exact=id_produto,
                )
                filiais_cod = se_vendas.values_list('cod_filial', flat=True).distinct()

                for filial in filiais_cod:
                    f = filial
                    lista_filiais.append(f)

                inf_filiais, total_vendas = a_multifiliais(cod_produto, cod_fornecedor, id_empresa,
                                             leadtime, t_reposicao, periodo, lista_filiais)

                # FILIAL SELECIONADA
                df_filial_selecionada = inf_filiais.query('filial == @filial_selecionada')
                df_filial_selecionada = df_filial_selecionada.drop(columns=[
                    'filial', 'estoque', 'avaria', 'saldo', 'dt_ult_entrada', 'qt_ult_entrada', 'vl_ult_entrada', 'dde',
                    'est_seguranca', 'p_reposicao', 'sugestao', 'sugestao_caixa', 'sugestao_unidade', 'preco_tabela',
                    'margem'
                ])

                i_filial_selec = df_filial_selecionada.to_dict('records')

                for i in i_filial_selec:
                    info_prod_filiais = i

                # TOTAL DE VENDAS X MES
                total_vendas['mes'] = total_vendas['mes'].astype(str)
                df_total_vendas = total_vendas.query('cod_filial == @filial_selecionada')

                lista_total_vendas = []

                for index, row in df_total_vendas.iterrows():
                    mes= row['mes'][4:]
                    ano= row['mes'][:4]
                    qt = row['qt_vendas']

                    dicionario = {
                        'mes': data_mes(mes),
                        'ano': ano,
                        'quantidade': qt
                    }
                    lista_total_vendas.append(dicionario)

                # TODAS AS FILIALS
                inf_filiais = inf_filiais.drop(columns=[
                    'curva', 'media_ajustada', 'ruptura_porc', 'ruptura_cor', 'condicao_estoque', 'porc_media',
                    'media_simples'
                ])

                inf_filiais = inf_filiais.to_dict('records')

                # ENVIO DE DADOS PARA JS
                data = []
                mapa = mapas_serie(id_empresa, cod_produto, filial_selecionada, periodo)

                data.append(inf_filiais)  # 0
                data.append(mapa)  # 1
                data.append(info_prod_filiais)  # 2
                data.append(lista_total_vendas)  # 3

                return JsonResponse({'data': data})
            else:
                zero = [0]
                return JsonResponse({'data': zero})

        except Exception as NameError:
            erro = str(NameError)
            d = [1, erro]

            return JsonResponse({'data': d})
    return JsonResponse({})


def data_mes(m):

    global mes
    n_mes = int(m)

    if n_mes == 1:
        mes = "Jan"
    elif n_mes == 2:
        mes = "Fev"
    elif n_mes == 3:
        mes = "Mar"
    elif n_mes == 4:
        mes = "Abr"
    elif n_mes == 5:
        mes = "Mai"
    elif n_mes == 6:
        mes = "Jun"
    elif n_mes == 7:
        mes = "Jul"
    elif n_mes == 8:
        mes = "Ago"
    elif n_mes == 9:
        mes = "Set"
    elif n_mes == 10:
        mes = "Out"
    elif n_mes == 11:
        mes = "Nov"
    elif n_mes == 12:
        mes = "Dez"

    return mes


def mapas_serie(id_empresa, cod_produto, cod_filial, periodo):
    info_prod = None
    lista_filiais = []
    lista_filiais.append(cod_filial)
    # df_vendas, info_produto = vendas(cod_produto, id_empresa, periodo, cod_filial)

    df_vendas, info_produto = vendas(cod_produto, id_empresa, periodo, lista_filiais)
    datas = dia_semana_mes_ano(id_empresa)
    df_historico = historico_estoque(cod_produto, id_empresa, periodo, lista_filiais)

    df_historico['data'] = pd.to_datetime(df_historico['data'], format='%Y-%m-%d')
    df_vendas['data'] = pd.to_datetime(df_vendas['data'], format='%Y-%m-%d')

    serie_estoque = pd.merge(datas, df_historico, how="left", on=["data"])

    serie_estoque['qt_estoque'].fillna(0, inplace=True)
    serie_estoque = serie_estoque.sort_values(by=['data'], ascending=True)

    data_day_est = serie_estoque['data'].copy()

    data_dia_est = data_day_est.dt.strftime('%d/%m/%Y')

    serie_estoque['data_serie_hist_est'] = serie_estoque['semana'].str.cat(data_dia_est, sep=" - ")

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
    qt_estoque = list(serie_estoque['qt_estoque'])
    label_dt_serie_est = list(serie_estoque['data_serie_hist_est'])

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
        'label_dt_serie_est': label_dt_serie_est,
        'periodo': periodo
    }

    return item


def add_prod_pedido_sessao(request):
    if request.is_ajax():
        produto_id = request.POST.get('produto')
        if produto_id != "0":

            cod_filial = request.POST.get('filial')
            qt_digitada = request.POST.get('qt_digitada')
            pr_compra = request.POST.get('pr_compra')

            qt_digitada = qt_digitada.replace(",", ".")
            qt_digitada = float(qt_digitada)

            preco_f = pr_compra.replace(",", ".")
            preco = float(preco_f)

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
                'ped_pr_compra': preco,
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
                preco = temp['ped_pr_compra']
                preco_form = locale.currency(preco, grouping=True)
                temp.update({'ped_pr_compra': preco_form})
                lista.append(temp)

            return JsonResponse({'data': lista})


def rm_prod_pedido_sessao(request):
    if request.is_ajax():
        produto_id = request.POST.get('produto')

        del request.session['pedido_produto'][produto_id]
        request.session.save()

        return JsonResponse({'data': 0})


def export_csv(request) -> object:
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="insight.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Pedido Insight')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # COLUNAS DA PLANILHA
    columns = ['cod_produto', 'preco', 'quantidade']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    # GET PEDIDO SESSÃO
    pedido = request.session.get('pedido_produto', [])
    lista = []

    id_usuario = request.user.usuario.id
    id_empresa = request.user.usuario.empresa_id

    empresa = Empresa.objects.get(id=id_empresa)
    usuario = User.objects.get(id=id_usuario)

    primeiro = usuario.first_name
    espaco = " "
    ultimo = usuario.last_name

    num_empresa = id_empresa
    num_empresa = str(num_empresa)
    num_user = str(id_usuario)

    data = datetime.datetime.now().strftime("%d%m%Y%H%M")

    # SALVAR EM PEDIDOS FEITOS
    p = PedidoInsight.objects.create(
        numero=f'{data}/{num_empresa}-{num_user}',
        usuario=primeiro + espaco + ultimo,
        empresa=empresa
    )
    p.save()

    # SALVAR ITENS DO PEDIDO
    for value in pedido.values():
        temp = value

        pr = temp['ped_pr_compra']
        preco = locale.currency(pr, grouping=True)

        p_i = PedidoInsightItens.objects.create(
            cod_produto=temp['ped_produto_cod'],
            desc_produto=temp['ped_produto_nome'],
            cod_filial=temp['ped_cod_filial'],
            preco=preco,
            quantidade=temp['ped_qt_digitada'],
            pedido=p
        )

        p_i.save()

        del [temp['ped_cod_filial']]
        del [temp['ped_produto_nome']]
        del [temp['ped_produto_id']]

        lista.append(temp)

    # LINHAS DA PLANILHA
    for row in lista:
        valores = row.values()
        l_valores = list(valores)
        row_num += 1

        for col_num in range(len(l_valores)):
            ws.write(row_num, col_num, l_valores[col_num], font_style)

    wb.save(response)

    del request.session['pedido_produto']
    request.session.save()

    return response


def pedidos_pedentes(request):
    empresa = request.user.usuario.empresa_id

    if request.is_ajax():
        produto_id = request.POST.get('produto')
        filial = request.POST.get('filial')

        if produto_id == "0":
            res = "FALSE"
            return JsonResponse({'data': res})

        else:
            prod_qs = Produto.objects.get(id=produto_id)
            produto_codigo = prod_qs.cod_produto

            pedidos = pedidos_todos(produto_codigo, empresa, filial)

            if pedidos is not None:

                pedidos['data'] = pd.to_datetime(pedidos.data).dt.strftime('%d/%m/%Y')
                pedidos.rename(columns={'data': 'data_ped'}, inplace=True)

                pedidos['data_ped'] = pedidos['data_ped'].astype(str)

                pedid = pedidos.assign(**pedidos.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict(
                    "records")

                return JsonResponse({'data': pedid})
            else:
                res = "NOTPEDIDO"
                return JsonResponse({'data': res})
    return JsonResponse({})