import math
import pandas as pd
from scipy.stats import norm
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def define_condicao_estoque(produto_resumo, tempo_reposicao, dde,
                            media, estoque_disponivel, dde_ponto_reposicao,
                            preco_custo, tempo_reposicao_fornecedor=''):
    """
        Função responsável por definir qual a codição do estoque do produto
    """
    if tempo_reposicao_fornecedor:
        if tempo_reposicao > tempo_reposicao_fornecedor:
            if tempo_reposicao < dde:
                tamanho = media * tempo_reposicao_fornecedor
                qt_excesso = estoque_disponivel - tamanho
                valor_e = qt_excesso * preco_custo

                vl_excesso = locale.currency(valor_e.round(2), grouping=True)

                produto_resumo['qt_excesso'] = qt_excesso.round(0)
                produto_resumo['quantidade_calc'] = qt_excesso.round(0)
                produto_resumo['vl_excesso'] = vl_excesso
                produto_resumo['sugestao'] = 0
                condicao_estoque = 'EXCESSO'

            elif tempo_reposicao >= dde > dde_ponto_reposicao:

                vl_excesso = locale.currency(0, grouping=True)
                produto_resumo['qt_excesso'] = 0
                produto_resumo['quantidade_calc'] = estoque_disponivel
                produto_resumo['vl_excesso'] = vl_excesso
                condicao_estoque = 'NORMAL'

            elif dde_ponto_reposicao >= dde > 0:
                vl_excesso = locale.currency(0, grouping=True)
                produto_resumo['qt_excesso'] = 0
                produto_resumo['quantidade_calc'] = estoque_disponivel
                produto_resumo['vl_excesso'] = vl_excesso
                condicao_estoque = 'PARCIAL'

            else:
                vl_excesso = locale.currency(0, grouping=True)
                produto_resumo['qt_excesso'] = 0
                produto_resumo['quantidade_calc'] = estoque_disponivel
                produto_resumo['vl_excesso'] = vl_excesso
                condicao_estoque = 'RUPTURA'

            produto_resumo['condicao_estoque'] = condicao_estoque

        else:
            if tempo_reposicao_fornecedor < dde:
                tamanho = media * tempo_reposicao_fornecedor
                qt_excesso = estoque_disponivel - tamanho
                valor_e = qt_excesso * preco_custo

                vl_excesso = locale.currency(valor_e.round(2), grouping=True)

                produto_resumo['qt_excesso'] = qt_excesso.round(0)
                produto_resumo['quantidade_calc'] = qt_excesso.round(0)
                produto_resumo['vl_excesso'] = vl_excesso
                produto_resumo['sugestao'] = 0
                condicao_estoque = 'EXCESSO'

            elif tempo_reposicao_fornecedor >= dde > dde_ponto_reposicao:
                vl_excesso = locale.currency(0, grouping=True)
                produto_resumo['qt_excesso'] = 0
                produto_resumo['quantidade_calc'] = estoque_disponivel
                produto_resumo['vl_excesso'] = vl_excesso
                condicao_estoque = 'NORMAL'

            elif dde_ponto_reposicao >= dde > 0:
                vl_excesso = locale.currency(0, grouping=True)
                produto_resumo['qt_excesso'] = 0
                produto_resumo['quantidade_calc'] = estoque_disponivel
                produto_resumo['vl_excesso'] = vl_excesso
                condicao_estoque = 'PARCIAL'

            else:
                vl_excesso = locale.currency(0, grouping=True)
                produto_resumo['qt_excesso'] = 0
                produto_resumo['quantidade_calc'] = estoque_disponivel
                produto_resumo['vl_excesso'] = vl_excesso
                condicao_estoque = 'RUPTURA'

            produto_resumo['condicao_estoque'] = condicao_estoque

    else:

        if tempo_reposicao < dde:
            tamanho = media * tempo_reposicao
            qt_excesso = estoque_disponivel - tamanho
            valor_e = qt_excesso * preco_custo

            produto_resumo['qt_excesso'] = qt_excesso.round(0)
            produto_resumo['quantidade_calc'] = qt_excesso.round(0)
            produto_resumo['vl_excesso'] = valor_e.round(2)
            condicao_estoque = 'EXCESSO'

        elif tempo_reposicao >= dde > dde_ponto_reposicao:
            produto_resumo['qt_excesso'] = 0
            produto_resumo['quantidade_calc'] = estoque_disponivel
            produto_resumo['vl_excesso'] = 0
            condicao_estoque = 'NORMAL'

        elif dde_ponto_reposicao >= dde > 0:

            produto_resumo['qt_excesso'] = 0
            produto_resumo['quantidade_calc'] = estoque_disponivel
            produto_resumo['vl_excesso'] = 0
            condicao_estoque = 'PARCIAL'

        else:
            produto_resumo['qt_excesso'] = 0
            produto_resumo['quantidade_calc'] = estoque_disponivel
            produto_resumo['vl_excesso'] = 0
            condicao_estoque = 'RUPTURA'

        produto_resumo['condicao_estoque'] = condicao_estoque

    resumo = produto_resumo.assign(**produto_resumo.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict(
        "records")

    return resumo


def calcula_estoque_seguranca(df_curva, parametros, leadtime, tempo_reposicao, desvio):
    """
        Função calcula o estoque de segurança do produto
    """

    curva_a = norm.ppf(parametros.curva_a / 100).round(3)
    curva_b = norm.ppf(parametros.curva_b / 100).round(3)
    curva_c = norm.ppf(parametros.curva_c / 100).round(3)
    curva_d = norm.ppf(parametros.curva_d / 100).round(3)
    curva_e = norm.ppf(parametros.curva_e / 100).round(3)

    if df_curva.curva.all() == "A":
        est_seg = curva_a * math.sqrt((leadtime + tempo_reposicao)) * desvio

    elif df_curva.curva.all() == "B":
        est_seg = curva_b * math.sqrt((leadtime + tempo_reposicao)) * desvio

    elif df_curva.curva.all() == "C":
        est_seg = curva_c * math.sqrt((leadtime + tempo_reposicao)) * desvio

    elif df_curva.curva.all() == "D":
        est_seg = curva_d * math.sqrt((leadtime + tempo_reposicao)) * desvio

    else:
        est_seg = curva_e * math.sqrt((leadtime + tempo_reposicao)) * desvio

    return est_seg.round(0)


def calcula_sugestao(produto_resumo, media, leadtime, estoque_seguranca, tempo_reposicao):
    """
        Função calcula a sugestão de compra para o produto
    """

    ponto_reposicao = (media * leadtime) + estoque_seguranca
    produto_resumo['ponto_repo'] = ponto_reposicao.round(0)

    sugestao = ((media * (leadtime + tempo_reposicao)) + estoque_seguranca) - (
            produto_resumo['saldo'] + produto_resumo['estoque_dispon'])

    return sugestao[0].round(0), ponto_reposicao


def soma_pedidos_pendentes(df_pedidos, filial):
    """
        Função soma quabtidades de saldo em pedidos pendentes
    """

    if not df_pedidos.empty:
        produto_resumo = df_pedidos.groupby(['cod_filial'])['saldo'].sum().round(2).to_frame().reset_index()
    else:
        pedido_vazio = {
            'cod_filial': filial,
            'saldo': 0
        }

        lista_pedido_vazio = [pedido_vazio]
        produto_resumo = pd.DataFrame.from_dict(lista_pedido_vazio)

    return produto_resumo


def organiza_informacoes_produto(produto_dados, lista_resumo):
    """
        Função organiza informações do produto que serão salvas no DB
    """

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
    quantidade_calc = str(produto_dados['quantidade_calc'].unique()).strip('[]')
    embalagem = str(produto_dados['embalagem'].unique()).strip('[]')
    valor_ult_entrada = float(produto_dados['vl_ult_ent'].unique())

    data = []
    itens_analise = {
        'embalagem': embalagem.replace("'", ""),
        'quantidade_caixa': qt_un_caixa,
        'filial': int(produto_dados['cod_filial'].unique()),
        'estoque': int(produto_dados['estoque_dispon'].unique()),
        'avaria': int(produto_dados['avarias'].unique()),
        'qt_bloqueada': int(produto_dados['qt_bloqueada'].unique()),
        'saldo': int(produto_dados['saldo'].unique()),
        'dt_ult_entrada': dt_u_entrada[0],
        'qt_ult_entrada': int(produto_dados['qt_ult_ent'].unique()),
        'vl_ult_entrada': round(valor_ult_entrada, 2),
        'dde': float(produto_dados['dde'].unique()),
        'est_seguranca': float(produto_dados['estoque_segur'].unique()),
        'p_reposicao': float(produto_dados['ponto_repo'].unique()),
        'sugestao': float(produto_dados['sugestao'].unique()),
        'sugestao_caixa': sug_cx,
        'sugestao_unidade': sug_unit,
        'valor_sugestao': valor_sugestao,
        'preco_tabela': float(produto_dados['preco_venda_tabela'].unique()),
        'custo': custo,
        'margem': float(produto_dados['margem'].unique()),
        'curva': curva.replace("'", ""),
        # 'media_ajustada': str(produto_dados['media_ajustada'].unique()).strip('[]'),
        'ruptura': ruptura.replace("'", ""),
        'ruptura_porc': float(produto_dados['ruptura_porc'].unique()),
        'ruptura_cor': str(produto_dados['cor_ruptura'].unique()).strip('[]'),
        'condicao_estoque': condicao_est.replace("'", ""),
        'porc_media': float(produto_dados['porcent_media'].unique()),
        'media_simples': float(produto_dados['media'].unique()),
        'qt_excesso': float(produto_dados['qt_excesso'].unique()),
        'vl_excesso': valor_excesso.replace("'", ""),
        'quantidade_calc': float(quantidade_calc.replace("'", ""))
    }

    data.append(itens_analise)

    lista_resumo.append(data)

    lista_fim = []
    for a in lista_resumo:
        for b in a:
            lista_fim.append(b)

    return lista_fim


def calcula_ruptura(df_vendas, df_info_produto, desvio, media, preco_custo, preco_tabela):
    # PORCENTAGEM DA MEDIA
    d_m = desvio / media
    por = 1.0 - d_m
    porcent_media = por * 100

    # CALCULO DE MARGEM
    m = preco_tabela - preco_custo
    m_ = m / preco_tabela
    margem = m_ * 100

    # DIAS SEM ESTOQUE / COM ESTOQUE / MEDIA DE PRECOS / PORCENTAGEM RUPTURA / DDE
    total_linha = df_vendas.shape[0]
    d_estoque = df_vendas['qt_estoque'].apply(lambda x: 0 if x <= 0 else 1).sum()
    d_sem_estoque = total_linha - d_estoque

    media_preco = df_info_produto.media_preco_praticado[0].round(2)
    variavel = media * media_preco
    ruptura = variavel * d_sem_estoque

    if ruptura > 0:
        cor_ruptura = 'negativo'
    else:
        cor_ruptura = 'positivo'

    porcent_ruptura = (d_sem_estoque / total_linha) * 100

    return porcent_media, porcent_ruptura, margem, cor_ruptura, ruptura


def total_vendas_mes(df_vendas):
    total_venda = df_vendas.copy()
    total_venda['data'] = pd.to_datetime(total_venda['data'])
    total_venda['mes'] = total_venda['data'].map(lambda x: 100 * x.year + x.month)
    total_vendas = total_venda.groupby(['mes', 'cod_filial'])['qt_vendas'].sum().reset_index()

    return total_vendas
