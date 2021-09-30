from django.db.models import Count
from api.models.pedido import Pedido
from core.models.empresas_models import Filial
import pandas as pd
import datetime


def pedidos_compra(cod_produto, id_empresa, lista_filiais):
    global lista_fim
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=90 - 1)  # Aqui sempre será o periodo informado -1

    # filiais = get_filiais(id_empresa)

    list = []
    for filial in lista_filiais:

        df = pd.DataFrame(Pedido.objects.all().filter(
            cod_produto__exact=cod_produto,
            cod_filial__exact=filial,
            data__range=[data_fim, data_inicio],
            empresa__id__exact=id_empresa
        ).order_by('-id').values())

        if not df.empty:
            # pedidos_df = df.drop_duplicates(subset=['num_pedido'], keep='first')
            pedido_ = df
            lista = pedido_.values.tolist()
            list.append(lista)

    lista_fim = []
    list_pedidos = []
    if list:


        for i in list:
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