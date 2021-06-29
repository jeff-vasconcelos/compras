from django.shortcuts import render
from core.multifilial.curva_abc import abc
from core.multifilial.estoque_atual import estoque_atual
from core.multifilial.historico_estoque import historico_estoque
from core.multifilial.pedidos import pedidos_compra
from core.multifilial.ultima_entrada import ultima_entrada
from core.multifilial.vendas import vendas
from core.models.parametros_models import Parametro
from scipy.stats import norm
import pandas as pd
import math
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def processa_produtos_filiais(request, template_name='aplicacao/paginas/teste_remover.html'):
    empresa = request.user.usuario.empresa_id
    forn = [16]
    produto = 180

    #CURVA ABC
    curva = abc(forn, empresa, 120)
    #lista_curva_abc = curva.to_dict('records')

    #ESTOQUE ATUAL
    est_atual_atual = estoque_atual(produto, empresa)
    #lista_est_atual = est_atual_atual.to_dict('records')

    #HISTORICO DE ESTOQUE
    h_estoque = historico_estoque(produto, empresa, 120)
    #lista_hist_estoq = h_estoque.to_dict('records')

    #PEDIDOS
    pedidos = pedidos_compra(produto, empresa)
    #lista_pedidos = pedidos.to_dict('records')

    #ULTIMAS ENTRADAS
    entradas = ultima_entrada(produto, empresa, 120)
    #lista_entradas = entradas.to_dict('records')

    #VENDAS
    venda, informacoes = vendas(produto, empresa, 120)
    #teste = venda.query("cod_filial == 1")
    #print(teste)
    #lista_informacoes_vendas = informacoes.to_dict('records')

    teste = dados_produto(180, 16, 1, 15, 30)
    print(teste)


    #
    # contexto = {
    #     'curva': lista_curva_abc,
    #     'estoque': lista_est_atual,
    #     'historico': lista_hist_estoq,
    #     'vendas': lista_informacoes_vendas,
    #     'pedidos': lista_pedidos,
    #     'entradas': lista_entradas
    # }
    return render(request, template_name)


def vendas_historico():
    df_vendas, informacoes_produto = vendas(180, 1, 120)
    df_historico = historico_estoque(180, 1, 120)

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



def dados_produto(cod_produto, cod_forn, id_empresa, leadt, t_reposicao):
    filial = 1
    cod_fornec = cod_forn
    cod_prod = cod_produto
    id_emp = id_empresa
    leadtime = leadt
    t_reposicao = t_reposicao

    # BUSCANDO PARAMETROS DA EMPRESA DO USUARIO LOGADO
    parametros = Parametro.objects.get(empresa_id=id_emp)

    # CARREGANDO DADOS DE OUTRAS FUNÇÕES
    pedidos = pedidos_compra(cod_prod, id_emp)
    u_entrada = ultima_entrada(cod_prod, id_emp, parametros.periodo)
    e_atual = estoque_atual(cod_prod, id_emp)
    vendas_p, info_produto = vendas_historico()

    print(info_produto)

    lista_fornecedor = []
    lista_fornecedor.append(cod_fornec)
    curva = abc(lista_fornecedor, id_emp, parametros.periodo)

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
        prod_resumo['media'] = media.round(2)
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
        #TODO Verificar coluna nas outras funções
        #preco_custo = e_atual.preco_custo[0]
        preco_custo = e_atual.custo_ult_ent[0]
        preco_tabela = e_atual.preco_venda[0]

        m = preco_tabela - preco_custo
        m_ = m / preco_tabela
        margem = m_ * 100
        prod_resumo['margem'] = margem.round(2)
        prod_resumo['preco_venda_tabela'] = preco_tabela.round(2)


        # DIAS SEM ESTOQUE / COM ESTOQUE / MEDIA DE PRECOS / PORCENTAGEM RUPTURA / DDE
        total_linha = vendas_p.shape[0]
        d_estoque = vendas_p['qt_estoque'].apply(lambda x: 0 if x <= 0 else 1).sum()
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
        #dde = estoque_disponivel / media_ajustada
        dde = estoque_disponivel / 1

        #TODO Precisa validar como dividir a media ajustada, quando o ela for 0


        ruptura = locale.currency(ruptura, grouping=True)
        prod_resumo['ruptura'] = ruptura
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

