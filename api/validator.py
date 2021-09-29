from api.models.produto import Produto
from api.models.fornecedor import Fornecedor
from api.models.estoque_atual import Estoque
from api.models.historico_estoque import HistoricoEstoque
from api.models.pedido_compra import Pedido
from api.models.ultima_entrada import Entrada
from api.models.venda import Venda
from api.models.pedidos import Pedidos_API


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

    histestoque = HistoricoEstoque.objects.filter(
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


def valida_pedido(data):
    cod_produto = data['cod_produto']
    cod_filial = data['cod_filial']
    cod_empresa = data['empresa']
    pedido = data['num_pedido']
    saldo = data['saldo']
    date = data['data']

    pedido = Pedido.objects.filter(
        cod_produto=cod_produto,
        cod_filial=cod_filial,
        empresa=cod_empresa,
        saldo=saldo,
        num_pedido=pedido,
        data=date
    ).exists()

    if pedido == False:
        return True
    else:
        pedido_existe = Pedidos_API.objects.filter(
            cod_produto=cod_produto,
            cod_filial=cod_filial,
            empresa=cod_empresa,
            saldo=saldo,
            num_pedido=pedido,
            data=date
        ).exists()

        if pedido_existe == False:
            b = Pedidos_API.objects.create(
                cod_produto = data['cod_produto'],
                cod_filial = data['cod_filial'],
                cod_fornecedor = data['cod_fornecedor'],
                saldo = data['saldo'],
                num_pedido = data['num_pedido'],
                data = data['data'],
                empresa = data['empresa']
            )
            b.save()

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
