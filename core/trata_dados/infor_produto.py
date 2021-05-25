from core.trata_dados.pedidos import pedidos_compras
from core.trata_dados.ultima_entrada import ultima_entrada
from core.trata_dados.estoque_atual import estoque_atual

import pandas as pd

from core.trata_dados.vendas import estatisca_vendas


def dados_produto():
    pedidos = pedidos_compras()
    u_entrada = ultima_entrada()
    e_atual = estoque_atual()
    info_prod,  = estatisca_vendas()

    if not pedidos.empty:
        if not u_entrada.empty:
            info_prod = pedidos.groupby(['cod_filial'])['saldo'].sum().round(2).to_frame().reset_index()

            estoque_a = e_atual['qt_disponivel'].to_frame().reset_index(drop=True)
            dt_ult_entrada = u_entrada['data'].unique()
            qt_ult_entrada = u_entrada['qt_ult_entrada'].unique()

            info_prod['avarias'] = e_atual['qt_indenizada'].sum()
            info_prod['estoque_dispon'] = estoque_a['qt_disponivel'] - info_prod['avarias']
            info_prod['dt_ult_ent'] = dt_ult_entrada
            info_prod['qt_ult_ent'] = qt_ult_entrada

            print(info_prod)

            media = pd.unique(vendas_datas_avarias_histo['media'])
            info_prod['dias_estoque_estim'] = (info_prod['estoque_dispon'] / media).round(0)

            return info_prod
        else:
            return None
    else:
        return