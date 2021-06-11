import datetime
from core.trata_dados.dados_produto import produto_dados
from core.trata_dados.pedidos import pedidos_compras
from core.trata_dados.ultima_entrada import ultima_entrada
from core.trata_dados.estoque_atual import estoque_atual
from core.trata_dados.curva_abc import abc
from core.models.parametros_models import Parametro
import pandas as pd
from scipy.stats import norm
import math


def dados_produto(cod_produto, cod_forn, id_empresa, leadt, t_reposicao):
    # PEGANDO DADOS DE PRODUTO, FORNCEDOR, EMPRESA E FUNCOES NECESSARIAS
    filial = 1
    cod_fornec = cod_forn
    cod_prod = cod_produto
    id_emp = id_empresa
    leadtime = leadt
    t_reposicao = t_reposicao

    # BUSCANDO PARAMETROS DA EMPRESA DO USUARIO LOGADO
    parametros = Parametro.objects.get(empresa_id=id_emp)

    # CARREGANDO DADOS DE OUTRAS FUNÇÕES
    pedidos, pedidos_all = pedidos_compras(cod_prod, id_emp, filial)
    u_entrada = ultima_entrada(cod_prod, id_emp, parametros.periodo)
    e_atual = estoque_atual(cod_prod, id_emp)
    vendas_p, info_produto = produto_dados(cod_prod, id_emp, parametros.periodo)
    curva = abc(cod_fornec, id_emp, parametros.periodo)

    # INFORMAÇÕES DE PRODUTO PARA AREA DE ANALISE
    # VALIDANDO DATAFRAMES
    if info_produto is not None:

        # VALIDANDO SE HOUVE ULTIMAS ENTRADAS
        if u_entrada is None:
            dt_ult_entrada = "-"
            qt_ult_entrada = 0
            vl_ult_entrada = 0
        else:
            dt_ult_entrada = u_entrada['data'].unique()
            qt_ult_entrada = u_entrada['qt_ult_entrada'].unique()
            vl_ult_entrada = u_entrada['vl_ult_entrada'].unique()

        # PEGANDO MEDIA, MEDIA AJUSTADA E DESVIO PADRAO
        media = info_produto.media[0]
        media_ajustada = info_produto.media_ajustada[0]
        desvio = info_produto.desvio[0]

        # SOMANDO SALDO DE PEDIDOS
        prod_resumo = pedidos.groupby(['cod_filial'])['saldo'].sum().round(2).to_frame().reset_index()

        # INFORMAÇÕES DE PRODUTO
        estoque_a = e_atual['qt_disponivel'].to_frame().reset_index(drop=True)
        prod_resumo['avarias'] = e_atual['qt_indenizada'].sum()
        prod_resumo['estoque_dispon'] = estoque_a['qt_disponivel'] - prod_resumo['avarias']
        prod_resumo['dt_ult_ent'] = dt_ult_entrada
        prod_resumo['qt_ult_ent'] = qt_ult_entrada
        prod_resumo['vl_ult_ent'] = vl_ult_entrada
        prod_resumo['dias_estoque_estim'] = (prod_resumo['estoque_dispon'] / media).round(0)

        # CALCULANDO ESTOQUE DE SEGURANÇA
        curva_a = norm.ppf(parametros.curva_a / 100).round(3)
        curva_b = norm.ppf(parametros.curva_b / 100).round(3)
        curva_c = norm.ppf(parametros.curva_c / 100).round(3)
        curva_d = norm.ppf(parametros.curva_d / 100).round(3)
        curva_e = norm.ppf(parametros.curva_e / 100).round(3)

        produto = curva.query('cod_produto == @cod_produto').reset_index(drop=True)

        if produto.curva[0] == "A":
            est_seg = curva_a * math.sqrt((leadtime + t_reposicao)) * desvio

        elif produto.curva[0] == "B":
            est_seg = curva_b * math.sqrt((leadtime + t_reposicao)) * desvio

        elif produto.curva[0] == "C":
            est_seg = curva_c * math.sqrt((leadtime + t_reposicao)) * desvio

        elif produto.curva[0] == "D":
            est_seg = curva_d * math.sqrt((leadtime + t_reposicao)) * desvio

        else:
            est_seg = curva_e * math.sqrt((leadtime + t_reposicao)) * desvio

        prod_resumo['estoque_segur'] = est_seg.round(0)

        # CALCULANDO PONTO DE REPOSIÇÃO

        estoque_segur = est_seg.round(0)
        ponto_reposicao = (media_ajustada * leadtime) + estoque_segur
        prod_resumo['ponto_repo'] = ponto_reposicao.round(0)

        # CALCULANDO SUGESTAO DE COMPRAS

        sugestao = ((media_ajustada * (leadtime + t_reposicao)) + estoque_segur) - (
                prod_resumo['saldo'] + prod_resumo['estoque_dispon'])

        prod_resumo['sugestao'] = sugestao[0].round(0)
        prod_resumo['media'] = media
        prod_resumo['media_ajustada'] = media_ajustada
        prod_resumo['desvio'] = desvio
        prod_resumo['curva'] = produto.curva[0]
        prod_resumo['qt_unit_caixa'] = info_produto.qt_unit_caixa[0]

        # PORCENTAGEM DA MEDIA
        d_m = desvio / media
        por = 1.0 - d_m
        porcent_media = por * 100
        prod_resumo['porcent_media'] = porcent_media.round(2)

        # CALCULO DE MARGEM
        preco_custo = e_atual.preco_custo[0]
        preco_tabela = e_atual.preco_venda[0]

        m = preco_tabela - preco_custo
        m_ = m / preco_tabela
        margem = m_ * 100
        prod_resumo['margem'] = margem.round(2)
        prod_resumo['preco_venda_tabela'] = preco_tabela

        # DIAS SEM ESTOQUE / COM ESTOQUE / MEDIA DE PRECOS / PORCENTAGEM RUPTURA / DDE
        total_linha = vendas_p.shape[0]
        d_estoque = vendas_p['qt_estoque'].apply(lambda x: 0 if x <= 0 else 1).sum()
        d_sem_estoque = total_linha - d_estoque

        media_preco = info_produto.media_preco_praticado[0].round(2)
        variavel = media * media_preco
        ruptura = variavel * d_sem_estoque
        porcent_ruptura = (d_sem_estoque / total_linha) * 100

        estoque_disponivel = prod_resumo.estoque_dispon[0]
        dde = estoque_disponivel / media_ajustada

        prod_resumo['ruptura'] = ruptura.round(2)
        prod_resumo['dde'] = dde.round(2)
        prod_resumo['ruptura_porc'] = porcent_ruptura.round(2)

        dde_ponto_rep = ponto_reposicao / media

        # DIFININDO CONDIÇÃO DE ESTOQUE
        if dde > dde_ponto_rep:
            condicao_estoque = 'NORMAL'
        elif dde_ponto_rep >= dde > 0:
            condicao_estoque = 'PARCIAL'
        else:
            condicao_estoque = 'RUPTURA'

        prod_resumo['condicao_estoque'] = condicao_estoque

        return prod_resumo

    else:
        return None
