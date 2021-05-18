from api.models.produto_models import *
from api.models.avarias_models import *


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

    avaria = Avaria.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa, data=data_avaria
    ).exists()

    if avaria == False:
        return True
    else:
        return False