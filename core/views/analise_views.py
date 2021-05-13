from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from api.models import *


def analise_painel(request, template_name='aplicacao/paginas/analise.html'):
    return render(request, template_name)


def buscar_produto(request):
    empresa = 1
    if request.is_ajax():
        res = None
        produto = request.POST.get('produto')
        qs = Produto.objects.filter(
            Q(desc_produto__icontains=produto) |
            Q(cod_produto__icontains=produto),
            Q(empresa__id__icontains=empresa)
        )
        if len(qs) > 0 and len(produto) > 0:
            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto,
                }
                data.append(item)
            res = data
        else:
            res = "Nada encontrado!"
        return JsonResponse({'data': res})
    return JsonResponse({})


def buscar_fornecedor(request):
    empresa = 1
    if request.is_ajax():
        res_f = None
        fornecedor = request.POST.get('fornecedor')
        qs = Fornecedor.objects.filter(
            Q(desc_fornecedor__icontains=fornecedor) |
            Q(cod_fornecedor__icontains=fornecedor),
            Q(empresa__id__icontains=empresa)
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
    empresa = 1
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
    empresa = 1
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
