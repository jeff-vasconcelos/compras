from django.shortcuts import render

from api.models.produto import Produto
from core.models.empresas_models import Filial
from core.multifilial.curva_abc import abc
from core.multifilial.estoque_atual import estoque_atual
from core.multifilial.historico_estoque import historico_estoque
from core.multifilial.pedidos import pedidos_compra
from core.multifilial.ultima_entrada import ultima_entrada
from core.multifilial.vendas import vendas
from core.multifilial.filiais import get_filiais
from core.models.parametros_models import Parametro
from scipy.stats import norm
import pandas as pd
import math
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def processa_produtos_filiais(id_produto, id_empresa, leadtime, t_reposicao, filialselecionada):

    produto_id = id_produto
    leadtime = leadtime
    temp_repo = t_reposicao
    filial_select = filialselecionada

    qs = Produto.objects.get(id=produto_id, empresa__id=id_empresa)

    produto_codigo = qs.cod_produto
    fornecedor_codigo = qs.cod_fornecedor

    informacaoes_produto = dados_produto(produto_codigo, fornecedor_codigo, id_empresa, leadtime, temp_repo, filial_select)

    filiais = get_filiais(id_empresa)

    contador = 0
    lista_resumo = []

    for filial in filiais:
        produto_dados = informacaoes_produto.query('cod_filial == @filial.cod_filial')

        if produto_dados is None:
            vazio = {'data': 0}
            return vazio

        else:
            dt_entrada = produto_dados['dt_ult_ent'][contador]
            if dt_entrada == '-':
                dt_u_entrada = dt_entrada
            else:
                dt_u_entrada = dt_entrada.strftime('%d/%m/%Y')

            sugestao = float(produto_dados['sugestao'])
            qt_un_caixa = float(produto_dados['qt_unit_caixa'])

            sug_cx = sugestao / qt_un_caixa
            sug_cx = math.ceil(sug_cx)
            sug_unit = sug_cx * qt_un_caixa

            data = []
            itens_analise = {
                'filial': int(produto_dados['cod_filial']),
                'estoque': int(produto_dados['estoque_dispon']),
                'avaria': int(produto_dados['avarias']),
                'saldo': int(produto_dados['saldo']),
                'dt_ult_entrada': dt_u_entrada,
                'qt_ult_entrada': int(produto_dados['qt_ult_ent']),
                'vl_ult_entrada': float(produto_dados['vl_ult_ent']),
                'dde': float(produto_dados['dde']),
                'est_seguranca': float(produto_dados['estoque_segur']),
                'p_reposicao': float(produto_dados['ponto_repo']),
                'sugestao': float(produto_dados['sugestao']),
                'sugestao_caixa': sug_cx,
                'sugestao_unidade': sug_unit,
                'preco_tabela': float(produto_dados['preco_venda_tabela'][contador]),
                'margem': float(produto_dados['margem'][contador]),
                'curva': str(produto_dados['curva'][contador]),
                'media_ajustada': str(produto_dados['media_ajustada'][contador]),
                'ruptura': str(produto_dados['ruptura'][contador]),
                'ruptura_porc': float(produto_dados['ruptura_porc']),
                'ruptura_cor': str(produto_dados['cor_ruptura'][contador]),
                'condicao_estoque': str(produto_dados['condicao_estoque'][contador]),
                'porc_media': float(produto_dados['porcent_media'][contador]),
                'media_simples': float(produto_dados['media'][contador]),
            }

            data.append(itens_analise)
            contador = contador + 1

            lista_resumo.append(data)

            lista_fim = []
            for a in lista_resumo:
                for b in a:
                    lista_fim.append(b)

    dados_produtos_filiais = pd.DataFrame(lista_fim)

    return dados_produtos_filiais



def vendas_historico(cod_prod, id_emp, periodo):
    df_vendas, informacoes_produto = vendas(cod_prod, id_emp, periodo)
    df_historico = historico_estoque(cod_prod, id_emp, periodo)

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
            columns=['id', 'produto_id', 'fornecedor_id', 'empresa_id', 'created_at', 'cod_fornecedor_y', 'filial_id'],
            inplace=True)

        return df_ven_hist, informacoes_produto

    else:
        return None, None


def dados_produto(cod_produto, cod_forn, id_empresa, leadt, t_reposicao, filial_selec):
    cod_fornec = cod_forn
    cod_prod = cod_produto
    id_emp = id_empresa

    filialselecionada = filial_selec


    # BUSCANDO PARAMETROS DA EMPRESA DO USUARIO LOGADO
    parametros = Parametro.objects.get(empresa_id=id_emp)

    # CARREGANDO DADOS DE OUTRAS FUNÇÕES
    pedidos = pedidos_compra(cod_prod, id_emp)
    u_entrada = ultima_entrada(cod_prod, id_emp, parametros.periodo)
    e_atual = estoque_atual(cod_prod, id_emp)
    vendas_p, info_produto = vendas_historico(cod_prod, id_emp, parametros.periodo)
    lista_fornecedor = []
    lista_fornecedor.append(cod_fornec)
    curva = abc(lista_fornecedor, id_emp, parametros.periodo)
    filiais = get_filiais(id_empresa)
    lista_resumo = []
    contador = 0
    media = 0

    if vendas_p is not None:
        for filial in filiais:
            vendas_ = vendas_p.query('cod_filial == @filial.cod_filial')
            curva_ = curva.query('cod_produto == @cod_produto & cod_filial == @filial.cod_filial') \
                .reset_index(drop=True)
            entradas_ = u_entrada.query('cod_filial == @filial.cod_filial')
            estoque_ = e_atual.query('cod_filial == @filial.cod_filial')

            if pedidos is not None:
                pedidos_ = pedidos.query('cod_filial == @filial.cod_filial')
            else:
                listped = []
                pedidos_ = pd.DataFrame(listped)

            #
            # if u_entrada is not None:
            #
            # else:
            #     listent = []
            #     entradas_ = pd.DataFrame(listent)
            #
            #
            # if e_atual is not None:
            #
            # else:
            #     listest = []
            #     estoque_ = pd.DataFrame(listest)
            #
            # print(estoque_)


            if entradas_.empty:
                dt_ult_entrada = "-"
                qt_ult_entrada = 0
                vl_ult_entrada = 0
            else:
                dt_ult_entrada = entradas_['data'].unique()
                qt_ult_entrada = entradas_['qt_ult_entrada'].unique()
                vl_ult_entrada = entradas_['vl_ult_entrada'].unique()


            if estoque_.empty:
                estoque_vazio = {
                    'cod_filial': filial.cod_filial,
                    'qt_disponivel': 0,
                    'qt_indenizada': 0
                }

                lista_est_vazio = [estoque_vazio]
                estoque_ = pd.DataFrame.from_dict(lista_est_vazio)


            if filial.cod_filial != filialselecionada:
                leadtime = 0
                temp_repo = 0
            else:
                leadtime = leadt
                temp_repo = t_reposicao

            # PEGANDO MEDIA, MEDIA AJUSTADA E DESVIO PADRAO
            media = info_produto.media[0]
            media_ajustada = info_produto.media_ajustada[0]
            desvio = info_produto.desvio[0]

            # SOMANDO SALDO DE PEDIDOS
            if not pedidos_.empty:
                prod_resumo = pedidos_.groupby(['cod_filial'])['saldo'].sum().round(2).to_frame().reset_index()
            else:
                pedido_vazio = {
                    'cod_filial': filial.cod_filial,
                    'saldo': 0
                }

                lista_pedido_vazio = [pedido_vazio]
                prod_resumo = pd.DataFrame.from_dict(lista_pedido_vazio)


            # INFORMAÇÕES DE PRODUTO

            estoque_a = estoque_['qt_disponivel'].to_frame().reset_index(drop=True)

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

            print(curva_.curva)

            if curva_.curva[0] == "A":
                est_seg = curva_a * math.sqrt((leadtime + temp_repo)) * desvio

            elif curva_.curva[0] == "B":
                est_seg = curva_b * math.sqrt((leadtime + temp_repo)) * desvio

            elif curva_.curva[0] == "C":
                est_seg = curva_c * math.sqrt((leadtime + temp_repo)) * desvio

            elif curva_.curva[0] == "D":
                est_seg = curva_d * math.sqrt((leadtime + temp_repo)) * desvio

            else:
                est_seg = curva_e * math.sqrt((leadtime + temp_repo)) * desvio

            prod_resumo['estoque_segur'] = est_seg.round(0)


            # CALCULANDO PONTO DE REPOSIÇÃO

            estoque_segur = est_seg.round(0)
            ponto_reposicao = (media_ajustada * leadtime) + estoque_segur
            prod_resumo['ponto_repo'] = ponto_reposicao.round(0)


            # CALCULANDO SUGESTAO DE COMPRAS

            sugestao = ((media_ajustada * (leadtime + temp_repo)) + estoque_segur) - (
                    prod_resumo['saldo'] + prod_resumo['estoque_dispon'])

            prod_resumo['sugestao'] = sugestao[0].round(0)
            prod_resumo['media'] = media.round(2)
            prod_resumo['media_ajustada'] = media_ajustada

            prod_resumo['desvio'] = desvio
            prod_resumo['curva'] = curva_.curva[0]
            prod_resumo['qt_unit_caixa'] = info_produto.qt_unit_caixa[0]

            # PORCENTAGEM DA MEDIA
            d_m = desvio / media
            por = 1.0 - d_m
            porcent_media = por * 100
            prod_resumo['porcent_media'] = porcent_media.round(2)



            # CALCULO DE MARGEM
            # TODO Verificar coluna nas outras funções
            # preco_custo = e_atual.preco_custo[0]

            preco_custo = estoque_.custo_ult_ent[contador]
            preco_tabela = estoque_.preco_venda[contador]

            #O contador vai navegar pelo indice do dataframe sempre inicando por 0, conforme a quantidade de filiais
            contador = contador + 1

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
            print(d_estoque)
            print(total_linha)
            ruptura = variavel * d_sem_estoque

            if ruptura > 0:
                cor_ruptura = 'negativo'
            else:
                cor_ruptura = 'positivo'

            prod_resumo['cor_ruptura'] = cor_ruptura

            porcent_ruptura = (d_sem_estoque / total_linha) * 100

            estoque_disponivel = prod_resumo.estoque_dispon[0]
            dde = estoque_disponivel / media_ajustada
            # dde = estoque_disponivel / 1

            # TODO Precisa validar como dividir a media ajustada, quando o ela for 0

            ruptura = locale.currency(ruptura, grouping=True)
            prod_resumo['ruptura'] = ruptura
            prod_resumo['dde'] = dde.round(2)
            prod_resumo['ruptura_porc'] = porcent_ruptura.round(2)

            print(ruptura)
            print(sugestao)
            print(media_ajustada)
            print(media)



            dde_ponto_rep = ponto_reposicao / media

            # DIFININDO CONDIÇÃO DE ESTOQUE
            if dde > dde_ponto_rep:
                condicao_estoque = 'NORMAL'
            elif dde_ponto_rep >= dde > 0:
                condicao_estoque = 'PARCIAL'
            else:
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

    else:
        return None