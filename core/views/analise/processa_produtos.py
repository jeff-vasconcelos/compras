from app.models.fornecedor import Fornecedor
from core.views.utils.estoque import estoque_atual
# from core.views.analise.pedidos import pedidos_compra
from core.views.analise.vendas import vendas
from core.models.parametros_models import Parametro
from core.views.utils.abc_functions import abc_fornecedores
from core.views.utils.produtos_functions import *
from core.views.utils.entradas import ultima_entrada
from core.views.utils.pedidos import pedidos_compra
import pandas as pd
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def a_multifiliais(cod_produto, cod_fornecedor, id_empresa, leadtime, tempo_reposicao, periodo, lista_filiais):
    global results
    informacaoes_produto, total_vendas = dados_produto(cod_produto, cod_fornecedor, id_empresa, leadtime,
                                                       tempo_reposicao, periodo, lista_filiais)

    lista_resumo = []

    for filial in lista_filiais:
        produto_dados = informacaoes_produto.query('cod_filial == @filial')

        results = organiza_informacoes_produto(produto_dados=produto_dados, lista_resumo=lista_resumo)

    dados_produtos_filiais = pd.DataFrame(results)

    return dados_produtos_filiais, total_vendas


def dados_produto(cod_produto, cod_fornecedor, id_empresa, leadtime, tempo_reposicao, periodo, lista_filiais):
    global resumo_produto, total_vendas, vendas_
    parametros = Parametro.objects.get(empresa_id=id_empresa)
    fornecedor = Fornecedor.objects.get(cod_fornecedor=cod_fornecedor, empresa__id__exact=id_empresa)

    # ja ajustados
    pedidos = pedidos_compra(cod_produto=cod_produto, id_empresa=id_empresa, lista_filiais=lista_filiais)
    u_entrada = ultima_entrada(cod_produto=cod_produto, id_empresa=id_empresa, periodo=periodo,
                               lista_filiais=lista_filiais)
    e_atual = estoque_atual(cod_produto=cod_produto, id_empresa=id_empresa, lista_filiais=lista_filiais)

    vendas_p, info_produto = vendas(cod_produto, id_empresa, periodo, lista_filiais)

    lista_fornecedor = []
    lista_resumo = []

    lista_fornecedor.append(cod_fornecedor)

    curva = abc_fornecedores(lista_fornecedor, id_empresa, periodo)

    for filial in lista_filiais:
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
        #media = info.media.unique()
        desvio = info.desvio.unique()

        # Função responsável por somar saldos de pedidos pendentes
        prod_resumo = soma_pedidos_pendentes(df_pedidos=pedidos_, filial=filial)

        # INFORMAÇÕES DE PRODUTO
        estoque_a = estoque_['qt_disponivel'].to_frame().reset_index(drop=True)
        prod_resumo['custo'] = estoque_['custo_ult_entrada'].unique()
        prod_resumo['avarias'] = estoque_['qt_indenizada'].sum()
        prod_resumo['estoque_dispon'] = estoque_a['qt_disponivel']
        prod_resumo['qt_bloqueada'] = estoque_['qt_bloqueada']
        prod_resumo['dt_ult_ent'] = dt_ult_entrada
        prod_resumo['qt_ult_ent'] = qt_ult_entrada
        prod_resumo['vl_ult_ent'] = vl_ult_entrada

        valida_media = math.isnan(info.media.unique())
        if not valida_media:
            media = info.media.unique()
            prod_resumo['media'] = media.round(2)
        else:
            media = 0.1
            prod_resumo['media'] = round(media, 2)

        prod_resumo['dias_estoque_estim'] = (prod_resumo['estoque_dispon'] / media).round(0)

        preco_custo = estoque_.custo_ult_entrada.unique()
        preco_tabela = estoque_.preco_venda.unique()

        # Função responsável por estoque de segurança
        estoque_seguranca = calcula_estoque_seguranca(df_curva=curva_, parametros=parametros,
                                                      leadtime=leadtime, tempo_reposicao=tempo_reposicao,
                                                      desvio=desvio)

        # Função responsável por calcular a sugestão e ponto de reposição
        sugestao, ponto_reposicao = calcula_sugestao(produto_resumo=prod_resumo, media=media, leadtime=leadtime,
                                                     tempo_reposicao=tempo_reposicao,
                                                     estoque_seguranca=estoque_seguranca)

        # Função calcula: margem, ruptura, porcentagem da media e ruptura
        porcent_media, porcent_ruptura, margem, cor_ruptura, ruptura = calcula_ruptura(df_vendas=vendas_,
                                                                                       df_info_produto=info_produto,
                                                                                       desvio=desvio,
                                                                                       media=media,
                                                                                       preco_custo=preco_custo,
                                                                                       preco_tabela=preco_tabela)

        estoque_disponivel = prod_resumo.estoque_dispon[0]
        dde = estoque_disponivel / media
        ruptura = locale.currency(ruptura, grouping=True)
        dde_ponto_rep = ponto_reposicao / media
        tempo_estoque_fornecedor = fornecedor.tempo_estoque
        tempo_reposicao_input = tempo_reposicao
        est_disponivel = prod_resumo['estoque_dispon'].unique()

        prod_resumo['sugestao'] = sugestao
        prod_resumo['media'] = media.round(2)
        prod_resumo['embalagem'] = info.embalagem.unique()
        prod_resumo['porcent_media'] = porcent_media.round(2)
        prod_resumo['desvio'] = desvio
        prod_resumo['curva'] = curva_.curva
        prod_resumo['margem'] = margem.round(2)
        prod_resumo['estoque_segur'] = estoque_seguranca
        prod_resumo['preco_venda_tabela'] = preco_tabela.round(2)
        prod_resumo['qt_unit_caixa'] = info.quantidade_un_caixa.unique()
        prod_resumo['ruptura'] = ruptura
        prod_resumo['dde'] = dde.round(2)
        prod_resumo['ruptura_porc'] = porcent_ruptura.round(2)
        prod_resumo['cor_ruptura'] = cor_ruptura

        # Função responsável pela classificação da condição de estoque
        results_condicao_estoque = define_condicao_estoque(produto_resumo=prod_resumo,
                                                           tempo_reposicao=tempo_reposicao_input,
                                                           dde=dde, media=media,
                                                           estoque_disponivel=est_disponivel,
                                                           dde_ponto_reposicao=dde_ponto_rep,
                                                           preco_custo=preco_custo,
                                                           tempo_reposicao_fornecedor=tempo_estoque_fornecedor
                                                           )

        lista_resumo.append(results_condicao_estoque)

        lista_fim = []
        for a in lista_resumo:
            for b in a:
                lista_fim.append(b)
        resumo_produto = pd.DataFrame(lista_fim)

    # Função reasponsável por calcular o total de vendas por mes dentro do periodo definido
    total_vendas = total_vendas_mes(df_vendas=vendas_p)

    return resumo_produto, total_vendas
