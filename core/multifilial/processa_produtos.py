from django.shortcuts import render
from core.multifilial.curva_abc import abc
from core.multifilial.estoque_atual import estoque_atual
from core.multifilial.historico_estoque import historico_estoque
from core.multifilial.pedidos import pedidos_compra
from core.multifilial.ultima_entrada import ultima_entrada
from core.multifilial.vendas import vendas
import pandas as pd


def processa_produtos_filiais(request, template_name='aplicacao/paginas/teste_remover.html'):
    empresa = request.user.usuario.empresa_id
    forn = [111]
    produto = 999

    #CURVA ABC
    curva = abc(forn, empresa, 90)
    lista_curva_abc = curva.to_dict('records')

    #ESTOQUE ATUAL
    est_atual_atual = estoque_atual(produto, empresa)
    lista_est_atual = est_atual_atual.to_dict('records')

    #HISTORICO DE ESTOQUE
    h_estoque = historico_estoque(produto, empresa, 90)
    lista_hist_estoq = h_estoque.to_dict('records')

    #PEDIDOS
    pedidos = pedidos_compra(produto, empresa)
    lista_pedidos = pedidos.to_dict('records')

    #ULTIMAS ENTRADAS
    entradas = ultima_entrada(produto, empresa, 90)
    lista_entradas = entradas.to_dict('records')

    #VENDAS
    venda, informacoes = vendas(produto, empresa, 90)
    #teste = venda.query("cod_filial == 1")
    #print(teste)
    lista_informacoes_vendas = informacoes.to_dict('records')

    teste, test = vendas_historico()
    teste_ = teste.query("cod_filial == 2")
    print(teste_['cod_filial'].unique())
    print(teste_['cod_filial'].count())

    contexto = {
        'curva': lista_curva_abc,
        'estoque': lista_est_atual,
        'historico': lista_hist_estoq,
        'vendas': lista_informacoes_vendas,
        'pedidos': lista_pedidos,
        'entradas': lista_entradas
    }
    return render(request, template_name, contexto)


def vendas_historico():
    df_vendas, informacoes_produto = vendas(999, 1, 90)
    df_historico = historico_estoque(999, 1, 90)
    cod_filial = 1

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
