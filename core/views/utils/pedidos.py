from api.models.pedido import Pedido
from core.views.alerta.verificador import get_filiais
import pandas as pd
import datetime


def pedidos_compra(cod_produto, id_empresa, lista_filiais=''):

    if lista_filiais:
        for filial in lista_filiais:
            results_lista = qs_pedidos(cod_produto=cod_produto, filial=filial,
                                       id_empresa=id_empresa)

        return process_pedidos(results_lista)

    else:

        filiais = get_filiais(id_empresa)

        for filial in filiais:
            results_lista = qs_pedidos(cod_produto=cod_produto, filial=filial.cod_filial,
                                       id_empresa=id_empresa)

        return process_pedidos(results_lista)


def qs_pedidos(cod_produto, filial, id_empresa):
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=90 - 1)
    lista_pedidos = []

    df = pd.DataFrame(Pedido.objects.all().filter(
        cod_produto__exact=cod_produto,
        cod_filial__exact=filial,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=id_empresa
    ).order_by('-id').values())

    if not df.empty:
        pedido_ = df
        lista = pedido_.values.tolist()
        lista_pedidos.append(lista)

    return lista_pedidos


def process_pedidos(lista_pedidos):
    list_pedidos = []
    lista_fim = []
    if lista_pedidos:

        for i in lista_pedidos:
            df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial", "cod_fornecedor", "saldo", "num_pedido",
                                          "data", "created_at","produto_id", "fornecedor_id", "filial_id", "empresa_id",
                                          "campo_um", "campo_dois", "campo_tres"
                                          ])

            df.drop(columns=["campo_um", "campo_dois", "campo_tres"], inplace=True)
            df = df.drop_duplicates(subset=['num_pedido'], keep='first')

            pedidos = df.groupby(['cod_filial'])['saldo'].sum().to_frame().reset_index()

            pedidos_ = pedidos.assign(
                **pedidos.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

            list_pedidos.append(pedidos_)


            for a in list_pedidos:
                for b in a:
                    lista_fim.append(b)

        pedidos = pd.DataFrame(lista_fim)
        pedidos = pedidos.drop_duplicates(subset=['cod_filial'], keep='first')

        return pedidos
    else:
        return None