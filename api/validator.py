from api.models.produto_models import *
from api.models.avarias_models import *
from api.models.estoque_atual_models import *
from api.models.hist_estoque_models import *
from api.models.p_compras_models import *
from api.models.ultima_entrada_models import *
from api.models.vendas_models import *


""" Função responsável por verificar se ja existe o registro no BD web, não permitindo duplicar
    informações vindas do  banco de dados local.
    
    Leva em consideração o codigo do produto, data de movimentação e filial
"""
def valida_produto(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']

    codproduto = Produto.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa
    ).exists()

    if codproduto == False:
        return True
    else:
        return False


def valida_fornecedor(data):
    cod_fornecedor = data['cod_fornecedor']
    cod_empresa = data['empresa']

    codfornecedor = Fornecedor.objects.filter(
        cod_fornecedor=cod_fornecedor, empresa=cod_empresa
    ).exists()

    if codfornecedor == False:
        return True
    else:
        return False


def valida_avaria(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']
    data_avaria = data['data']
    print("codigo da empresa ", cod_empresa)

    avaria = Avaria.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa
    ).exists()

    if avaria == False:
        return True
    else:
        return False


def valida_estoque_atual(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']
    data = data['data']

    estoqueatual = EstoqueAtual.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa, data=data
    ).exists()

    if estoqueatual == False:
        return True
    else:
        return False


def valida_hist_estoque(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']
    data = data['data']

    histestoque = HistEstoque.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa, data=data
    ).exists()

    if histestoque == False:
        return True
    else:
        return False


def valida_pedido(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']
    data = data['data']

    pedido = PedidoCompras.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa, data=data
    ).exists()

    if pedido == False:
        return True
    else:
        return False


def valida_ultentrada(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']
    data = data['data']

    ultentrada = UltimaEntrada.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa, data=data
    ).exists()

    if ultentrada == False:
        return True
    else:
        return False


def valida_venda(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']
    data = data['data']

    venda = Venda.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa, data=data
    ).exists()

    if venda == False:
        return True
    else:
        return False