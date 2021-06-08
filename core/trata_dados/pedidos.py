from django.db.models import Count

from api.models.p_compras_models import PedidoCompras
import pandas as pd
import datetime


def pedidos_compras(cod_produto, id_empresa, cod_filial):

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=90 - 1) #Aqui sempre será o periodo informado -1

    df = pd.DataFrame(PedidoCompras.objects.all().filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa,
        cod_filial=cod_filial,
        data__range=[data_fim, data_inicio]
    ).order_by('-id').values())

    pedidos_df = df.drop_duplicates(subset=['num_pedido'], keep='first')

    if not pedidos_df.empty:
        pedidos = pedidos_df.groupby(['cod_filial'])['saldo'].sum().to_frame().reset_index()

        print("PEDIDOS - OK")
        print("##############################")

        return pedidos
    else:
        pedido_vazio = {
            'cod_produto': cod_produto, 'cod_filial': cod_filial, 'saldo': 0
        }
        pedido_vazio_df = pd.DataFrame([pedido_vazio])

        print("PEDIDOS - O PRODUTO NÃO TEM PEDIDOS PENDENTES")
        print("##############################")

    return pedido_vazio_df