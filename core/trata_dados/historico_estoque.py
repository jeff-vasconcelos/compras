from api.models.historico_estoque import HistoricoEstoque
import pandas as pd
import datetime


def historico_estoque(cod_produto, id_empresa, periodo):
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    h_estoque = pd.DataFrame(HistoricoEstoque.objects.filter(
        cod_produto__exact=cod_produto,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=id_empresa
    ).values())

    if not h_estoque.empty:

        print("HISTORICO ESTOQUE - OK")
        print("##############################")

        return h_estoque
    else:
        print("HISTORICO ESTOQUE - O PRODUTO NÃO TEM HISTORICO ESTOQUE")
        print("##############################")

        return None