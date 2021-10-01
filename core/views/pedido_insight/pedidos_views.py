import locale
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from api.models.fornecedor import Fornecedor
from api.models.produto import Produto
from core.models.pedidos_models import *
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


@login_required
def pedido_painel(request, template_name='aplicacao/paginas/pedidos/pedidos.html'):
    id_empresa = request.user.usuario.empresa_id
    pedidos = PedidoInsight.objects.filter(empresa__id=id_empresa)

    contexto = {
        'pedidos': pedidos
    }

    return render(request, template_name, contexto)


@login_required
def ver_pedidos_insight(request, pk, template_name='aplicacao/paginas/pedidos/ver-pedido.html'):
    pedido = PedidoInsight.objects.get(id=pk)
    itens = ItemPedidoInsight.objects.filter(pedido=pedido.pk)

    contexto = {
        'itens':itens,
        'pedido': pedido
    }

    return render(request, template_name, contexto)


def add_prod_pedido_sessao(request):
    if request.is_ajax():
        produto_id = request.POST.get('produto')

        if produto_id != "0":

            cod_filial = request.POST.get('filial')
            qt_digitada = request.POST.get('qt_digitada')
            pr_compra = request.POST.get('pr_compra')

            qt_digitada = qt_digitada.replace(",", ".")
            qt_digitada = float(qt_digitada)

            preco_f = pr_compra.replace(".", "")
            preco_f = preco_f.replace(",", ".")
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


def pedido_save_db(request) -> object:
    if request.is_ajax():
        id_fornecedor = request.POST.get('fornecedor')

        # GET PEDIDO SESSÃO
        pedido = request.session.get('pedido_produto', [])
        lista = []

        id_usuario = request.user.usuario.id
        id_empresa = request.user.usuario.empresa_id

        empresa = Empresa.objects.get(id=id_empresa)
        usuario = User.objects.get(id=id_usuario)
        fornecedor = Fornecedor.objects.get(id=id_fornecedor)

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
            campo_um=fornecedor.cod_fornecedor,
            campo_dois=fornecedor.desc_fornecedor,
            empresa=empresa
        )
        p.save()

        # SALVAR ITENS DO PEDIDO
        for value in pedido.values():
            temp = value

            pr = temp['ped_pr_compra']
            preco = locale.currency(pr, grouping=True)

            p_i = ItemPedidoInsight.objects.create(
                cod_produto=temp['ped_produto_cod'],
                desc_produto=temp['ped_produto_nome'],
                cod_filial=temp['ped_cod_filial'],
                preco=preco,
                quantidade=temp['ped_qt_digitada'],
                pedido=p
            )

            p_i.save()

            lista.append(temp)

    return JsonResponse({})