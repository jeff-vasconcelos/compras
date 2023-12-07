import locale
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from app.models.fornecedor import Fornecedor
from app.models.produto import Produto
from core.models.pedidos_models import *

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


@login_required
def pedido_painel(request, template_name='aplicacao/paginas/pedidos/pedidos.html'):
    id_empresa = request.user.usuario.empresa_id
    pedidos = PedidoInsight.objects.filter(empresa__id=id_empresa).order_by('-id')

    contexto = {
        'pedidos': pedidos
    }

    return render(request, template_name, contexto)


@login_required
def ver_pedidos_insight(request, pk, template_name='aplicacao/paginas/pedidos/ver-pedido.html'):
    pedido = PedidoInsight.objects.get(id=pk)
    itens = ItemPedidoInsight.objects.filter(pedido=pedido.pk)

    contexto = {
        'itens': itens,
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


def add_pedido_sessao_fornecedores(request):
    if request.is_ajax():
        produto_id = request.POST.get('produtos')

        if produto_id != "":

            # PEGANDO E TRATANDO DADOS DE FILIAIS DA REQUISIÇÃO
            filial = request.POST.get('filiais')
            l_filiais = get_data_request(filial)
            lista_filiais = convert_data_request_int(l_filiais)

            # PEGANDO E TRATANDO DADOS DE PRODUTOS DA REQUISIÇÃO
            idprod = request.POST.get('produtos')
            l_produtos = get_data_request(idprod)
            lista_produtos = convert_data_request_int(l_produtos)


            # PEGANDO E TRATANDO DADOS DE QUANTIDADE DA REQUISIÇÃO
            quantidade = request.POST.get('quantidades')
            l_quantidade = get_data_request(quantidade)
            lista_quantidade = convert_data_request_float(l_quantidade)

            # PEGANDO E TRATANDO DADOS DE PRECOS DA REQUISIÇÃO
            precos = request.POST.get('precos')
            l_precos = get_data_request(precos)
            lista_precos = convert_data_request_float(l_precos)

            # VERIFICANDO SE CAMPOS TEM QUANTIDADES COMPATIVEIS
            if len(lista_quantidade) != len(lista_precos):
                res = "FALHOU"
                return JsonResponse({'data': res})

            # SESSAO
            if not request.session.get('pedido_produto'):
                request.session['pedido_produto'] = {}
                request.session.save()

            pedido = request.session['pedido_produto']

            for (f, p, q , r) in zip(lista_filiais, lista_produtos, lista_quantidade, lista_precos):

                produto_qs = Produto.objects.get(id=p)

                pedido[produto_qs.id] = {
                    'ped_produto_id': produto_qs.id,
                    'ped_produto_cod': produto_qs.cod_produto,
                    'ped_produto_nome': produto_qs.desc_produto,
                    'ped_cod_filial': f,
                    'ped_pr_compra': r,
                    'ped_qt_digitada': q,
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


def pedido_save_db(request):
    global data
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
        data = "SUCESSO"
    return JsonResponse({'data': data})


def get_data_request(lista):
    data_req = lista.replace(",", " ")
    data_req = data_req.split()
    lista_requisicao = []
    for dr in data_req:
        lista_requisicao.append(dr)

    return lista_requisicao

def convert_data_request_int(lista):
    lista_int = []
    for i in lista:
        lista_int.append(int(i))

    return lista_int


def convert_data_request_float(lista):
    lista_float = []
    for i in lista:
        lista_float.append(float(i))

    return lista_float