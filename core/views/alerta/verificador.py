import datetime
from api.models.fornecedor import Fornecedor
from core.models.empresas_models import Filial
from api.models.produto import Produto
from api.models.estoque import Estoque
from api.models.venda import Venda
from core.models.parametros_models import Parametro


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
        empresa__id__exact=id_empresa,
        is_active=True
    )

    estoque = Estoque.objects.filter(
        cod_produto__exact=cod_produto,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=id_empresa
    ).order_by('-id')

    politica_fornecedor = produto.fornecedor.tempo_estoque

    if politica_fornecedor is not None:
        if vendas and estoque:
            return True
        else:
            return False
    else:
        return False


def check_sales_by_period(company_id, product):
    parameters = Parametro.objects.get(empresa_id=company_id)

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=parameters.periodo - 1)

    sales = Venda.objects.filter(
        cod_produto__exact=product.cod_produto,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=company_id
    ).exists()

    if sales:
        return True
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

