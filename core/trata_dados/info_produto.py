from core.trata_dados.datas import dia_semana_mes_ano
from core.trata_dados.vendas import estatisca_vendas
from core.trata_dados.avarias import avarias
from core.trata_dados.hist_estoque import historico_estoque
from core.trata_dados.pedidos import pedidos_compras


import pandas as pd


def produto_info():
    df_vendas, infor = estatisca_vendas()
    df_avarias = avarias()
    df_historico = historico_estoque()

    df_vendas['data'] = pd.to_datetime(df_vendas['data'], format='%Y-%m-%d')
    df_avarias['data'] = pd.to_datetime(df_avarias['data'], format='%Y-%m-%d')
    df_historico['data'] = pd.to_datetime(df_historico['data'], format='%Y-%m-%d')

    df_vendas_avarias = pd.merge(df_vendas, df_avarias, how="left", on=["data"])
    df_vendas_avarias.fillna(0, inplace=True)

    df_ven_ava_hist = pd.merge(df_vendas_avarias, df_historico, how="left", on=["data"])
    values = {'qt_est_disponivel': 0}
    df_ven_ava_hist.fillna(value=values, inplace=True)


    return df_ven_ava_hist