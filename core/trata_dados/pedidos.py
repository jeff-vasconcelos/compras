from api.models.p_compras_models import PedidoCompras
import pandas as pd
import datetime


def pedidos_compras():

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=119) #Aqui sempre será o periodo informado -1

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    pedidos_df = pd.DataFrame(PedidoCompras.objects.filter(
        cod_produto__exact=183,
        empresa__id__exact=1,
        data__range=[data_fim, data_inicio]
    ).values())

    if not pedidos_df.empty:
        pedidos = pedidos_df.groupby(['cod_filial'])['saldo'].sum().to_frame().reset_index()

        return pedidos
    else:
        print("O produto não tem pedidos de compras pendentes!")
        return None