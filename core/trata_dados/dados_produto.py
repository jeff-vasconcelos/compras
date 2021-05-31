from core.trata_dados.datas import dia_semana_mes_ano
from core.trata_dados.vendas import vendas
from core.trata_dados.avarias import avarias
from core.trata_dados.hist_estoque import historico_estoque
from core.trata_dados.pedidos import pedidos_compras
import pandas as pd


def produto_dados():
    df_vendas, infor = vendas()
    df_avarias = avarias()
    df_historico = historico_estoque()
    df_pedidos = pedidos_compras()

    if not df_vendas.empty:
        if not df_avarias.empty:

            df_vendas['data'] = pd.to_datetime(df_vendas['data'], format='%Y-%m-%d')
            df_avarias['data'] = pd.to_datetime(df_avarias['data'], format='%Y-%m-%d')
            df_historico['data'] = pd.to_datetime(df_historico['data'], format='%Y-%m-%d')

            df_vendas_avarias = pd.merge(df_vendas, df_avarias, how="left",
                                         on=["data", "cod_produto", "cod_filial", "desc_produto"])
            df_vendas_avarias.fillna(0, inplace=True)

            df_ven_ava_hist = pd.merge(df_vendas_avarias, df_historico, how="left",
                                       on=["data", "cod_produto", "cod_filial", "desc_produto"])

            values = {'qt_est_disponivel': 0, 'qt_estoque': 0}
            df_ven_ava_hist.fillna(value=values, inplace=True)
            df_ven_ava_hist.drop(columns=['id', 'produto_id', 'fornecedor_id', 'empresa_id', 'created_at', 'cod_fornecedor_y'], inplace=True)

            #print(df_ven_ava_hist)
            return df_ven_ava_hist
        else:
            return None
    else:
        return None

