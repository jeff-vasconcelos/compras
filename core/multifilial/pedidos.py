from django.db.models import Count
from api.models.pedido_compra import Pedido
from core.models.empresas_models import Filial
import pandas as pd
import datetime


def pedidos_compra(cod_produto, id_empresa):

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=90 - 1) #Aqui sempre será o periodo informado -1

    df = pd.DataFrame(Pedido.objects.all().filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa,
        data__range=[data_fim, data_inicio]
    ).order_by('-id').values())

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    pedidos_df = df.drop_duplicates(subset=['num_pedido'], keep='first')

    if not pedidos_df.empty:

        list = []
        for filial in filiais:
            pedido_ = pedidos_df
            pedido_ = pedido_.query('cod_filial == @filial.cod_filial')
            lista = pedido_.values.tolist()
            list.append(lista)

        list_pedidos = []
        for i in list:
            df = pd.DataFrame(i, columns=["id", "cod_produto", "desc_produto", "cod_filial", "filial_id",
                                          "cod_fornecedor", "produto_id", "fornecedor_id", "empresa_id", "saldo",
                                          "num_pedido", "data", "created_at"])

            pedidos = df.groupby(['cod_filial'])['saldo'].sum().to_frame().reset_index()

            pedidos_ = pedidos.assign(
                **pedidos.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

            list_pedidos.append(pedidos_)

            lista_fim = []
            for a in list_pedidos:
                for b in a:
                    lista_fim.append(b)

        pedidos = pd.DataFrame(lista_fim)

        return pedidos
    else:
        return None