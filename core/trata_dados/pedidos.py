from django.db.models import Count

from api.models.p_compras_models import PedidoCompras
import pandas as pd
import datetime


def pedidos_compras(cod_produto, id_empresa, periodo):

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1) #Aqui sempre será o periodo informado -1

    df = pd.DataFrame(PedidoCompras.objects.all().filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa,
        data__range=[data_fim, data_inicio]
    ).order_by('-id').values())

    print(df)

    pedidos_df = df.drop_duplicates(subset=['num_pedido'], keep='first')

    print(pedidos_df)

    if not pedidos_df.empty:
        pedidos = pedidos_df.groupby(['cod_filial'])['saldo'].sum().to_frame().reset_index()

        return pedidos
    else:
        print("O produto não tem pedidos de compras pendentes!")
    return None