import datetime
from api.models.fornecedor import Fornecedor
from core.models.empresas_models import Filial
from api.models.produto import Produto
from api.models.venda import Venda


def verifica_produto(cod_produto, id_empresa, periodo):

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    vendas =Venda.objects.filter(
        cod_produto__exact=cod_produto,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=id_empresa
    ).exists()

    produto = Produto.objects.get(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa
    )

    politica_fornecedor = produto.fornecedor.tempo_estoque

    if politica_fornecedor is not None:
        if vendas:
            return True
        else:
            return False
    else:
        return False


def get_produtos(id_empresa, id_fornecedor):
    produtos = Produto.objects.filter(
        empresa__id__exact=id_empresa,
        fornecedor__id__exact=id_fornecedor
    )
    return produtos


def get_filiais(id_empresa):
    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)
    return filiais


def get_fornecedores(id_empresa):
    qs_fornec = Fornecedor.objects.filter(empresa__id__exact=id_empresa)
    lista_fornecedores = []
    for f in qs_fornec:
        lista_fornecedores.append(f.cod_fornecedor)
    return lista_fornecedores


def get_fornecedores_qs(id_empresa):
    qs_fornec = Fornecedor.objects.filter(empresa__id__exact=id_empresa)
    return qs_fornec

