from api.models.hist_estoque_models import HistEstoque
import pandas as pd
import datetime


def historico_estoque():
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=119)  # Aqui sempre será o periodo informado -1

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    h_estoque = pd.DataFrame(HistEstoque.objects.filter(
        cod_produto__exact=2042,
        empresa__id__exact=2,
        data__range=[data_fim, data_inicio]
    )[:1].values())

    if not h_estoque.empty:
        return h_estoque
    else:
        print("O produto não tem registro de estoque!")
        return None