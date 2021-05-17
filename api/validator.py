from api.models.produto_models import *
from django.db.models import Q


""" Função responsável por verificar se ja existe o registro no BD web, não permitindo duplicar
    informações vindas do  banco de dados local.
    
    Leva em consideração o codigo do produto, data de movimentação e filial
"""
def valida_produto(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']

    #codproduto = Produto.objects.filter(Q(cod_produto=cod_produto) & (Q(desc_produto=desc_produto))).exists()
    codproduto = Produto.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa
    ).exists()

    if codproduto == False:
        return True
    else:
        return False
