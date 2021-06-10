from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from api.models.fornecedor_models import *
from api.models.produto_models import *

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

        qs = Produto.objects.get(id=produto, empresa__id=empresa)
        print(produto)
        print(qs.cod_produto)

        produto_codigo = qs.cod_produto
        fornecedor_codigo = qs.cod_fornecedor
        leadtime = 0
        t_reposicao = 0

        produto_dados = dados_produto(produto_codigo, fornecedor_codigo, empresa, leadtime, t_reposicao)

        if produto_dados is None:
            print("O produto não pode ser analisado! O produto pode não ter vendas.")
            print(produto_dados)

            data = []
            item = {
                'pk': '',
                'nome': '',
                'cod': '',
                'emb': '',
                'filial': ''
            }
            data.append(item)
            info_prod = data

            return JsonResponse({'data': info_prod})

        else:
            print(produto_dados)

            data = []
            item = {
                'pk': qs.pk,
                'nome': qs.desc_produto,
                'cod': qs.cod_produto,
                'emb': qs.embalagem,
                'filial': qs.cod_filial
            }
            data.append(item)
            info_prod = data

            return JsonResponse({'data': info_prod})

    return JsonResponse({})


def mapa_serie(request):
    label_max = []
    data_max = []
    label_med = []
    data_med = []
    label_min = []
    data_min = []
    label_preco = []
    data_preco = []
    label_custo = []
    data_custo = []
    label_lucro = []
    data_lucro = []
    label_qtvenda = []
    data_qtvenda = []
    empresa = request.user.usuario.empresa_id
    if request.is_ajax():
        info_prod = None
        produto = request.POST.get('produto')


        vendas(produto, empresa)