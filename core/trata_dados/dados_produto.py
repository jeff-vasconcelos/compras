from core.trata_dados.vendas import vendas
from core.trata_dados.hist_estoque import historico_estoque
import pandas as pd
import datetime


def produto_dados(cod_produto, id_empresa, periodo):
    df_vendas, info_produto = vendas(cod_produto, id_empresa, periodo)
    df_historico = historico_estoque(cod_produto, id_empresa, periodo)
    cod_filial = 1

    if df_vendas is not None:
        df_vendas['data'] = pd.to_datetime(df_vendas['data'], format='%Y-%m-%d')
        df_historico['data'] = pd.to_datetime(df_historico['data'], format='%Y-%m-%d')

        # df_vendas_avarias = pd.merge(df_vendas, df_avarias, how="left",
        #                              on=["data", "cod_produto", "cod_filial", "desc_produto"])
        # df_vendas_avarias.fillna(0, inplace=True)

        df_ven_hist = pd.merge(df_vendas, df_historico, how="left",
                                   on=["data", "cod_produto", "cod_filial", "desc_produto"])
        embalagem = df_historico['embalagem'][0]

        values = {'embalagem': embalagem, 'qt_est_disponivel': 0, 'qt_estoque': 0}

        df_ven_hist.fillna(value=values, inplace=True)
        df_ven_hist.drop(
            columns=['id', 'produto_id', 'fornecedor_id', 'empresa_id', 'created_at', 'cod_fornecedor_y'],
            inplace=True)

        print("PRODUTOS DADOS - AVARIAS/VENDAS OK")
        print("##############################")

        return df_ven_hist, info_produto
    else:
        return None, None

