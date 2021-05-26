import math

from core.trata_dados.pedidos import pedidos_compras
from core.trata_dados.ultima_entrada import ultima_entrada
from core.trata_dados.estoque_atual import estoque_atual
from core.trata_dados.curva_abc import abc

import pandas as pd

from core.trata_dados.vendas import estatisca_vendas


def dados_produto():
    pedidos = pedidos_compras()
    u_entrada = ultima_entrada()
    e_atual = estoque_atual()
    vendas, infor_prod = estatisca_vendas()

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

            media = infor_prod.media[0]

            info_prod['dias_estoque_estim'] = (info_prod['estoque_dispon'] / media).round(0)
            print(info_prod)

            return info_prod
        else:
            return None
    else:
        return


def estoque_seguranca():
    info_prod = dados_produto()
    curva = abc()
    vendas, infor_prod = estatisca_vendas()
    #
    #curva_a = norm.ppf(0.75).round(3)
    # curva_b = norm.ppf(0.85).round(3)
    # curva_c = norm.ppf(0.50).round(3)
    # curva_d = norm.ppf(0.50).round(3)
    # curva_e = norm.ppf(0.50).round(3)
    #
    # leadtime = 15
    # t_reposicao = 25
    #
    # produto = curva.cod_produto
    # desvio = infor_prod.desvio
    #
    # if produto.curva[0] == "A":
    #     est_seg = curva_a * math.sqrt((leadtime + t_reposicao)) * desvio
    #
    # elif produto.curva[0] == "B":
    #     est_seg = curva_b * math.sqrt((leadtime + t_reposicao)) * desvio
    #
    # elif produto.curva[0] == "C":
    #     est_seg = curva_c * math.sqrt((leadtime + t_reposicao)) * desvio
    #
    # elif produto.curva[0] == "D":
    #     est_seg = curva_d * math.sqrt((leadtime + t_reposicao)) * desvio
    #
    # else:
    #     est_seg = curva_e * math.sqrt((leadtime + t_reposicao)) * desvio
    #
    # info_prod['estoque_segur'] = est_seg.round(0)
    print(info_prod)
    return info_prod

def ponto_reposicao():
    infor_prod = estoque_seguranca()
