from core.trata_dados.pedidos import pedidos_compras
from core.trata_dados.ultima_entrada import ultima_entrada
from core.trata_dados.estoque_atual import estoque_atual
from core.trata_dados.curva_abc import abc
from core.trata_dados.vendas import vendas
import pandas as pd
#from scipy.stats import norm
import math


def dados_produto(cod, empresa):
    id_prod = cod
    id_emp = empresa
    print("IDs produto e empresa", id_prod, id_emp)
    pedidos = pedidos_compras()
    u_entrada = ultima_entrada()
    e_atual = estoque_atual()
    vendas_p, info_produto = vendas(id_prod, id_emp)
    curva = abc()
    leadtime = 15
    t_reposicao = 25

    # INFORMÇÕES GERAIS

    if pedidos is not None:
        if info_produto is not None:
            if not u_entrada.empty:

                media = info_produto.media[0]
                # media_ajustada = info_produto.media_ajustada[0]
                # desvio = info_produto.desvio[0]
                #
                # prod_resumo = pedidos.groupby(['cod_filial'])['saldo'].sum().round(2).to_frame().reset_index()
                #
                # estoque_a = e_atual['qt_disponivel'].to_frame().reset_index(drop=True)
                # dt_ult_entrada = u_entrada['data'].unique()
                # qt_ult_entrada = u_entrada['qt_ult_entrada'].unique()
                #
                # prod_resumo['avarias'] = e_atual['qt_indenizada'].sum()
                # prod_resumo['estoque_dispon'] = estoque_a['qt_disponivel'] - prod_resumo['avarias']
                # prod_resumo['dt_ult_ent'] = dt_ult_entrada
                # prod_resumo['qt_ult_ent'] = qt_ult_entrada
                #
                # prod_resumo['dias_estoque_estim'] = (prod_resumo['estoque_dispon'] / media).round(0)
                #
                # print("PASSOU - INFORMACOES GERAIS")
                #
                # # ESTOQUE DE SEGURANÇA
                #
                # curva_a = norm.ppf(0.75).round(3)
                # curva_b = norm.ppf(0.85).round(3)
                # curva_c = norm.ppf(0.50).round(3)
                # curva_d = norm.ppf(0.50).round(3)
                # curva_e = norm.ppf(0.50).round(3)
                #
                # produto = curva.cod_produto
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
                # prod_resumo['estoque_segur'] = est_seg.round(0)
                #
                # print("PASSOU - ESTOQUE DE SEGURANÇA")
                #
                # # PONTO DE REPOSIÇÃO
                #
                # estoque_segur = est_seg.round(0)
                #
                # ponto_reposicao = (media_ajustada * leadtime) + estoque_segur
                #
                # prod_resumo['ponto_repo'] = ponto_reposicao.round(0)
                #
                # print("PASSOU - PONTO DE REPOSICAO")
                #
                # # SUGESTAO DE COMPRAS
                #
                # sugestao = ((media_ajustada * (leadtime + t_reposicao)) + estoque_segur) - (
                #             prod_resumo['saldo'] + prod_resumo['estoque_dispon'])
                #
                # prod_resumo['sugestao'] = sugestao[0].round(0)
                # prod_resumo['media'] = media
                # prod_resumo['media_ajustada'] = media_ajustada
                # prod_resumo['desvio'] = desvio
                #
                # print("PASSOU - SUGESTAO DE COMPRAS")
                #
                print("FUNCIONANDO - DEF DADOS_PROD")
                return media

            else:
                print("SEM DADOS ULT ENTRADA - DEF DADOS_PROD")
                return None
        else:
            print("SEM DADOS VENDAS - DEF DADOS_PROD")
            return None
    else:
        print("SEM DADOS PEDIDOS - DEF DADOS_PROD")
        return None