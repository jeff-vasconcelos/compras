from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from api.models import *


def analise_painel(request, template_name='aplicacao/paginas/analise.html'):
    return render(request, template_name)


def search_produto(request):
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


def search_fornecedor(request):
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


def filter_produto_fornecedor(request):
    empresa = 1
    if request.is_ajax():
        res_fil_fornec = None
        fornecedor = request.POST.get('fornecedor')
        print(fornecedor)
        qs = Produto.objects.filter(
            Q(fornecedor_id__exact=fornecedor),
            Q(empresa__id__exact=empresa)
        )
        if len(qs) > 0 and len(fornecedor) > 0:
            data = []
            for prod in qs:
                item = {
                    'pk': prod.pk,
                    'nome': prod.desc_produto,
                    'cod': prod.cod_produto
                }
                data.append(item)
            res_fil_fornec = data
        else:
            res_fil_fornec = "Nada encontrado!"
        return JsonResponse({'data': res_fil_fornec})
    return JsonResponse({})

"""
def get_produto_fornecedor(request, *args, **kwargs):
    empresa = 1
    fornecedor = kwargs.get('fornec')
    produto_obj = list(Produto.objects.filter(fornecedor_id=fornecedor, empresa_id=empresa).values())
    return JsonResponse({'data': produto_obj})
"""