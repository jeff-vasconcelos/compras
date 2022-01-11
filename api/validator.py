from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque import Estoque
from api.models.historico import Historico
from api.models.pedido import Pedido
from api.models.entrada import Entrada
from api.models.venda import Venda
# from api.models.pedido_duplicado import PedidoDuplicado


def valida_produto(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']

    qs_produto = Produto.objects.filter(
        cod_produto=cod_produto, empresa=cod_empresa
    ).exists()

    if not qs_produto:
        return True
    else:
        update_product(data)
        return False


def valida_fornecedor(data):
    cod_fornecedor = data['cod_fornecedor']
    cod_empresa = data['empresa']

    qs_fornecedor = Fornecedor.objects.filter(
        cod_fornecedor=cod_fornecedor, empresa=cod_empresa
    ).exists()

    if not qs_fornecedor:
        return True
    else:
        update_fornecedor(data)
        return False


def valida_estoque_atual(data):
    cod_produto = data['cod_produto']
    cod_filial = data['cod_filial']
    quantidade = data['qt_geral']
    cod_empresa = data['empresa']
    date = data['data']

    estoqueatual = Estoque.objects.filter(
        cod_produto=cod_produto,
        cod_filial=cod_filial,
        empresa=cod_empresa,
        data=date,
        qt_geral=quantidade
    ).exists()

    if estoqueatual == False:
        return True
    else:
        return False


def valida_hist_estoque(data):
    cod_produto = data['cod_produto']
    cod_filial = data['cod_filial']
    cod_empresa = data['empresa']
    quantidade = data['qt_estoque']
    date = data['data']

    histestoque = Historico.objects.filter(
        cod_produto=cod_produto,
        cod_filial=cod_filial,
        empresa=cod_empresa,
        qt_estoque=quantidade,
        data=date
    ).exists()

    if histestoque == False:
        return True
    else:
        return False


def validate_order(data):

    buy_order = Pedido.objects.filter(
        cod_produto=data['cod_produto'],
        cod_filial=data['cod_filial'],
        empresa=data['empresa'],
        num_pedido=data['num_pedido'],
        saldo=data['saldo'],
        data=data['data']
    ).exists()

    if not buy_order:
        return True
    else:
        return False


def valida_ultentrada(data):
    cod_produto = data['cod_produto']
    cod_filial = data['cod_filial']
    cod_empresa = data['empresa']
    quantidade = data['qt_ult_entrada']
    fornec = data['cod_fornecedor']
    date = data['data']

    ultentrada = Entrada.objects.filter(
        cod_produto=cod_produto,
        cod_filial=cod_filial,
        empresa=cod_empresa,
        data=date,
        qt_ult_entrada=quantidade,
        cod_fornecedor=fornec
    ).exists()

    if ultentrada == False:
        return True
    else:
        return False


def valida_venda(data):
    cod_produto = data['cod_produto']
    cod_empresa = data['empresa']
    cod_filial = data['cod_filial']
    dt = data['data']
    qt = data['qt_venda']
    preco = data['preco_unit']
    cli = data['cliente']
    nf = data['num_nota']

    venda = Venda.objects.filter(
        cod_produto=cod_produto,
        empresa=cod_empresa,
        cod_filial=cod_filial,
        data=dt,
        qt_venda=qt,
        preco_unit=preco,
        cliente=cli,
        num_nota=nf
    ).exists()

    if venda == False:
        return True
    else:
        return False


def update_product(data):
    qs_produto = Produto.objects.get(
        cod_produto__exact=data['cod_produto'],
        empresa=data['empresa']
    )

    qs_produto.desc_produto = data['desc_produto']
    qs_produto.embalagem = data['embalagem']
    qs_produto.quantidade_un_cx = data['quantidade_un_cx']
    qs_produto.marca = data['marca']
    qs_produto.peso_liquido = data['peso_liquido']
    qs_produto.principio_ativo = data['principio_ativo']
    qs_produto.cod_fabrica = data['cod_fabrica']
    qs_produto.cod_fornecedor = data['cod_fornecedor']
    qs_produto.cod_auxiliar = data['cod_auxiliar']
    qs_produto.cod_depto = data['cod_depto']
    qs_produto.cod_sec = data['cod_sec']
    qs_produto.cod_depto = data['cod_depto']
    qs_produto.desc_departamento = data['desc_departamento']
    qs_produto.desc_secao = data['desc_secao']

    qs_produto.save()


def update_fornecedor(data):
    qs_fornecedor = Fornecedor.objects.get(
        cod_fornecedor__exact=data['cod_fornecedor'],
        empresa=data['empresa']
    )

    qs_fornecedor.desc_fornecedor = data['desc_fornecedor']
    qs_fornecedor.cnpj = data['cnpj']
    qs_fornecedor.iestadual = data['iestadual']

    qs_fornecedor.save()
