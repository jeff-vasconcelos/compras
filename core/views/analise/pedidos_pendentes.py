from app.models.pedido import Pedido
from app.models.produto import Produto
import pandas as pd
import datetime


def pedidos_todos(cod_produto, id_empresa, cod_filial):
    global lista_fim
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=90 - 1)  # Aqui sempre será o periodo informado -1

    df = pd.DataFrame(Pedido.objects.all().filter(
        cod_produto__exact=cod_produto,
        cod_filial__exact=cod_filial,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=id_empresa
    ).order_by('-id').values())

    if not df.empty:

        produto = Produto.objects.get(
            cod_produto__exact=cod_produto,
            empresa__id__exact=id_empresa
        )

        pedidos = df.sort_values(by=['data'], ascending=False)

        pedidos = pedidos.drop_duplicates(subset=['num_pedido'], keep='first')

        indexNames = pedidos[(pedidos['saldo'] == 0)].index
        pedidos.drop(indexNames, inplace=True)

        pedidos['desc_produto'] = produto.desc_produto

        # pedidos = pedidos.drop_duplicates(subset=['num_pedido'], keep='first')

        return pedidos
    else:
        return None