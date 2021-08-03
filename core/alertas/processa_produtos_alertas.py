from datetime import time

import numpy as np
from django.shortcuts import render

from api.models.fornecedor import Fornecedor
from api.models.produto import Produto
from core.alertas.curva_abc_alertas import abc
from core.alertas.estoque_atual_alertas import estoque_atual
from core.alertas.historico_estoque_alertas import historico_estoque
from core.alertas.pedidos_alertas import pedidos_compra
from core.alertas.ultima_entrada_alertas import ultima_entrada
from core.alertas.vendas_alertas import vendas
from core.alertas.verificador import get_filiais
from core.models.parametros_models import Parametro
from scipy.stats import norm
import pandas as pd
import math
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def processa_produtos_filiais(cod_produto, cod_fornecedor, id_empresa, leadtime, tempo_reposicao, periodo):
    global dt_u_entrada
    informacaoes_produto = dados_produto(cod_produto, cod_fornecedor, id_empresa, leadtime, tempo_reposicao, periodo)

    lista_resumo = []

    filiais = []
    for i, v in informacaoes_produto.cod_filial.iteritems():
        filiais.append(v)

    for filial in filiais:
        produto_dados = informacaoes_produto.query('cod_filial == @filial')

        dt_entrada = produto_dados['dt_ult_ent'].unique()

        if dt_entrada == '-':
            dt_u_entrada = dt_entrada
        else:
            t = pd.to_datetime(dt_entrada)
            dt_u_entrada = t.strftime('%d/%m/%Y')


        sugestao = float(produto_dados['sugestao'].unique())
        qt_un_caixa = float(produto_dados['qt_unit_caixa'].unique())
        custo = float(produto_dados['custo'].unique())

        sug_cx = sugestao / qt_un_caixa

        sug_cx = math.ceil(sug_cx)

        sug_unit = sug_cx * qt_un_caixa

        valor_sugestao = sug_unit * custo

        curva = str(produto_dados['curva'].unique()).strip('[]')
        ruptura = str(produto_dados['ruptura'].unique()).strip('[]')
        condicao_est = str(produto_dados['condicao_estoque'].unique()).strip('[]')
        valor_excesso = str(produto_dados['vl_excesso'].unique()).strip('[]')

        data = []
        itens_analise = {
            'filial': int(produto_dados['cod_filial'].unique()),
            'estoque': int(produto_dados['estoque_dispon'].unique()),
            'avaria': int(produto_dados['avarias'].unique()),
            'saldo': int(produto_dados['saldo'].unique()),
            'dt_ult_entrada': dt_u_entrada[0],
            'qt_ult_entrada': int(produto_dados['qt_ult_ent'].unique()),
            'vl_ult_entrada': float(produto_dados['vl_ult_ent'].unique()),
            'dde': float(produto_dados['dde'].unique()),
            'est_seguranca': float(produto_dados['estoque_segur'].unique()),
            'p_reposicao': float(produto_dados['ponto_repo'].unique()),
            'sugestao': float(produto_dados['sugestao'].unique()),
            'sugestao_caixa': sug_cx,
            'sugestao_unidade': sug_unit,
            'valor_sugestao': valor_sugestao,
            'preco_tabela': float(produto_dados['preco_venda_tabela'].unique()),
            'custo':custo,
            'margem': float(produto_dados['margem'].unique()),
            'curva': curva.replace("'", ""),
            'media_ajustada': str(produto_dados['media_ajustada'].unique()).strip('[]'),
            'ruptura': ruptura.replace("'", ""),
            'ruptura_porc': float(produto_dados['ruptura_porc'].unique()),
            'ruptura_cor': str(produto_dados['cor_ruptura'].unique()).strip('[]'),
            'condicao_estoque': condicao_est.replace("'", ""),
            'porc_media': float(produto_dados['porcent_media'].unique()),
            'media_simples': float(produto_dados['media'].unique()),
            'qt_excesso': float(produto_dados['qt_excesso'].unique()),
            'vl_excesso': valor_excesso.replace("'", ""),
        }

        data.append(itens_analise)

        lista_resumo.append(data)

        lista_fim = []
        for a in lista_resumo:
            for b in a:
                lista_fim.append(b)

    dados_produtos_filiais = pd.DataFrame(lista_fim)

    return dados_produtos_filiais


def dados_produto(cod_produto, cod_fornecedor, id_empresa, leadtime, tempo_reposicao, periodo):
    global resumo_produto, qt_excesso, vl_excesso
    parametros = Parametro.objects.get(empresa_id=id_empresa)
    fornecedor = Fornecedor.objects.get(cod_fornecedor=cod_fornecedor)
    pedidos = pedidos_compra(cod_produto, id_empresa)
    u_entrada = ultima_entrada(cod_produto, id_empresa, periodo)
    e_atual = estoque_atual(cod_produto, id_empresa)
    vendas_p, info_produto = vendas(cod_produto, id_empresa, periodo)

    lista_fornecedor = []
    lista_resumo = []

    lista_fornecedor.append(cod_fornecedor)
    curva = abc(lista_fornecedor, id_empresa, periodo)

    filiais = []
    for i, v in info_produto.cod_filial.iteritems():
        filiais.append(v)

    for filial in filiais:
        if pedidos is not None:
            pedidos_ = pedidos.query('cod_filial == @filial')
        else:
            pedidos_ = pd.DataFrame()

        if u_entrada is not None:
            entradas_ = u_entrada.query('cod_filial == @filial')
        else:
            entradas_ = pd.DataFrame()

        vendas_ = vendas_p.query('cod_filial == @filial')

        estoque_ = e_atual.query('cod_filial == @filial')
        curva_ = curva.query('cod_produto == @cod_produto & cod_filial == @filial') \
            .reset_index(drop=True)

        if entradas_.empty:
            dt_ult_entrada = "-"
            qt_ult_entrada = 0
            vl_ult_entrada = 0
        else:
            dt_ult_entrada = entradas_['data'].unique()
            qt_ult_entrada = entradas_['qt_ult_entrada'].unique()
            vl_ult_entrada = entradas_['vl_ult_entrada'].unique()

        # PEGANDO MEDIA, MEDIA AJUSTADA E DESVIO PADRAO
        info = info_produto.query('cod_filial == @filial')

        media = info.media.unique()
        media_ajustada = info.media_ajustada.unique()
        desvio = info.desvio.unique()

        # SOMANDO SALDO DE PEDIDOS
        if not pedidos_.empty:
            prod_resumo = pedidos_.groupby(['cod_filial'])['saldo'].sum().round(2).to_frame().reset_index()
        else:
            pedido_vazio = {
                'cod_filial': filial,
                'saldo': 0
            }

            lista_pedido_vazio = [pedido_vazio]
            prod_resumo = pd.DataFrame.from_dict(lista_pedido_vazio)

        # INFORMAÇÕES DE PRODUTO

        estoque_a = estoque_['qt_disponivel'].to_frame().reset_index(drop=True)
        prod_resumo['custo'] = estoque_['custo_ult_entrada'].unique()

        prod_resumo['avarias'] = estoque_['qt_indenizada'].sum()
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

        if curva_.curva.all() == "A":
            est_seg = curva_a * math.sqrt((leadtime + tempo_reposicao)) * desvio

        elif curva_.curva.all() == "B":
            est_seg = curva_b * math.sqrt((leadtime + tempo_reposicao)) * desvio

        elif curva_.curva.all() == "C":
            est_seg = curva_c * math.sqrt((leadtime + tempo_reposicao)) * desvio

        elif curva_.curva.all() == "D":
            est_seg = curva_d * math.sqrt((leadtime + tempo_reposicao)) * desvio

        else:
            est_seg = curva_e * math.sqrt((leadtime + tempo_reposicao)) * desvio

        prod_resumo['estoque_segur'] = est_seg.round(0)

        valida_media = math.isnan(media_ajustada)

        # CALCULANDO PONTO DE REPOSIÇÃO
        estoque_segur = est_seg.round(0)

        if valida_media == False:
            ponto_reposicao = (media_ajustada * leadtime) + estoque_segur
            prod_resumo['ponto_repo'] = ponto_reposicao.round(0)

            # CALCULANDO SUGESTAO DE COMPRAS
            sugestao = ((media_ajustada * (leadtime + tempo_reposicao)) + estoque_segur) - (
                    prod_resumo['saldo'] + prod_resumo['estoque_dispon'])
        else:
            ponto_reposicao = (media * leadtime) + estoque_segur
            prod_resumo['ponto_repo'] = ponto_reposicao.round(0)

            # CALCULANDO SUGESTAO DE COMPRAS
            sugestao = ((media * (leadtime + tempo_reposicao)) + estoque_segur) - (
                    prod_resumo['saldo'] + prod_resumo['estoque_dispon'])


        prod_resumo['sugestao'] = sugestao[0].round(0)
        prod_resumo['media'] = media.round(2)
        prod_resumo['media_ajustada'] = media_ajustada

        prod_resumo['desvio'] = desvio
        prod_resumo['curva'] = curva_.curva
        prod_resumo['qt_unit_caixa'] = info.quantidade_un_caixa.unique()

        # PORCENTAGEM DA MEDIA
        d_m = desvio / media
        por = 1.0 - d_m
        porcent_media = por * 100
        prod_resumo['porcent_media'] = porcent_media.round(2)

        # CALCULO DE MARGEM
        preco_custo = estoque_.custo_ult_entrada.unique()
        preco_tabela = estoque_.preco_venda.unique()

        m = preco_tabela - preco_custo
        m_ = m / preco_tabela
        margem = m_ * 100
        prod_resumo['margem'] = margem.round(2)
        prod_resumo['preco_venda_tabela'] = preco_tabela.round(2)

        # DIAS SEM ESTOQUE / COM ESTOQUE / MEDIA DE PRECOS / PORCENTAGEM RUPTURA / DDE
        total_linha = vendas_.shape[0]
        d_estoque = vendas_['qt_estoque'].apply(lambda x: 0 if x <= 0 else 1).sum()
        d_sem_estoque = total_linha - d_estoque

        media_preco = info_produto.media_preco_praticado[0].round(2)
        variavel = media * media_preco
        ruptura = variavel * d_sem_estoque

        if ruptura > 0:
            cor_ruptura = 'negativo'
        else:
            cor_ruptura = 'positivo'

        prod_resumo['cor_ruptura'] = cor_ruptura

        porcent_ruptura = (d_sem_estoque / total_linha) * 100

        estoque_disponivel = prod_resumo.estoque_dispon[0]

        if media_ajustada <= 0:
            dde = estoque_disponivel / media
        else:
            dde = estoque_disponivel / media_ajustada

        ruptura = locale.currency(ruptura, grouping=True)
        prod_resumo['ruptura'] = ruptura
        prod_resumo['dde'] = dde.round(2)
        prod_resumo['ruptura_porc'] = porcent_ruptura.round(2)

        dde_ponto_rep = ponto_reposicao / media

        temp_est = fornecedor.tempo_estoque
        est_disponivel = prod_resumo['estoque_dispon'].unique()


        if temp_est < dde:
            tamanho = media_ajustada * temp_est
            qt_excesso = est_disponivel - tamanho
            valor_e = qt_excesso * preco_custo

            vl_e = valor_e.round(2)
            vl_excesso = locale.currency(vl_e, grouping=True)

            prod_resumo['qt_excesso'] = qt_excesso.round(0)
            prod_resumo['vl_excesso'] = vl_excesso
            condicao_estoque = 'EXCESSO'

        elif temp_est >= dde > dde_ponto_rep:
            vl_e = 0
            vl_excesso = locale.currency(vl_e, grouping=True)
            prod_resumo['qt_excesso'] = 0
            prod_resumo['vl_excesso'] = vl_excesso
            condicao_estoque = 'NORMAL'

        elif dde_ponto_rep >= dde > 0:
            vl_e = 0
            vl_excesso = locale.currency(vl_e, grouping=True)
            prod_resumo['qt_excesso'] = 0
            prod_resumo['vl_excesso'] = vl_excesso
            condicao_estoque = 'PARCIAL'

        else:
            vl_e = 0
            vl_excesso = locale.currency(vl_e, grouping=True)
            prod_resumo['qt_excesso'] = 0
            prod_resumo['vl_excesso'] = vl_excesso
            condicao_estoque = 'RUPTURA'

        prod_resumo['condicao_estoque'] = condicao_estoque

        resumo = prod_resumo.assign(**prod_resumo.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict(
            "records")

        lista_resumo.append(resumo)

        lista_fim = []
        for a in lista_resumo:
            for b in a:
                lista_fim.append(b)
        resumo_produto = pd.DataFrame(lista_fim)

    return resumo_produto
