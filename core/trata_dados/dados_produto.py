from core.trata_dados.vendas import vendas
from core.trata_dados.avarias import avarias
from core.trata_dados.hist_estoque import historico_estoque
import pandas as pd
import datetime


def produto_dados(cod_produto, id_empresa, periodo):
    df_vendas, info_produto = vendas(cod_produto, id_empresa, periodo)
    df_avarias = avarias(cod_produto, id_empresa, periodo)
    df_historico = historico_estoque(cod_produto, id_empresa, periodo)
    cod_filial = 1

    if df_vendas is not None:
        df_vendas['data'] = pd.to_datetime(df_vendas['data'], format='%Y-%m-%d')
        df_historico['data'] = pd.to_datetime(df_historico['data'], format='%Y-%m-%d')

        # SE AVARIAS FOR VAZIO
        if df_avarias is None:
            dt = datetime.date.today()
            cod_p = cod_produto
            desc_p = df_vendas['desc_produto'].unique()
            cod_f = (cod_filial)
            qt_a = 0

            avarias_vazio = {
                'data': dt, 'cod_produto': cod_p, 'desc_produto': desc_p[0], 'cod_filial': cod_f, 'qt_avaria': qt_a
            }

            df_avarias = pd.DataFrame([avarias_vazio])
            df_avarias['data'] = pd.to_datetime(df_avarias['data'], format='%Y-%m-%d')

            print("PRODUTOS DADOS - AVARIAS VAZIO")
            print("##############################")

        else:
            df_avarias['data'] = pd.to_datetime(df_avarias['data'], format='%Y-%m-%d')

        df_vendas_avarias = pd.merge(df_vendas, df_avarias, how="left",
                                     on=["data", "cod_produto", "cod_filial", "desc_produto"])
        df_vendas_avarias.fillna(0, inplace=True)

        df_ven_ava_hist = pd.merge(df_vendas_avarias, df_historico, how="left",
                                   on=["data", "cod_produto", "cod_filial", "desc_produto"])

        values = {'qt_est_disponivel': 0, 'qt_estoque': 0}
        df_ven_ava_hist.fillna(value=values, inplace=True)
        df_ven_ava_hist.drop(
            columns=['id', 'produto_id', 'fornecedor_id', 'empresa_id', 'created_at', 'cod_fornecedor_y'],
            inplace=True)

        print("PRODUTOS DADOS - AVARIAS/VENDAS OK")
        print("##############################")

        return df_ven_ava_hist, info_produto
    else:
        return None, None

