import locale
from api.models.fornecedor import Fornecedor
from core.views.alerta.vendas import vendas
from core.models.parametros_models import Parametro
from core.views.alerta.verificador import get_fornecedores_qs, get_produtos, verifica_produto
from core.views.utils.produtos_functions import *
from core.views.utils.abc_functions import abc_fornecedores, abc_home
from core.views.utils.entradas import ultima_entrada
from core.views.utils.pedidos import pedidos_compra
from core.views.utils.estoque import estoque_atual

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def processa_produtos_filiais(cod_produto, cod_fornecedor, id_empresa, leadtime, tempo_reposicao, periodo, curva_filial, curva_home):
    """

    """
    global results
    informacaoes_produto = dados_produto(cod_produto, cod_fornecedor,
                                         id_empresa, leadtime,
                                         tempo_reposicao, periodo, curva_filial, curva_home)

    lista_resumo = []

    filiais = []
    for i, v in informacaoes_produto.cod_filial.iteritems():
        filiais.append(v)

    for filial in filiais:
        produto_dados = informacaoes_produto.query('cod_filial == @filial')

        results = organiza_informacoes_produto(produto_dados=produto_dados, lista_resumo=lista_resumo)

    dados_produtos_filiais = pd.DataFrame(results)

    return dados_produtos_filiais


def dados_produto(cod_produto, cod_fornecedor, id_empresa, leadtime, tempo_reposicao, periodo, curva_filial, curva_home):
    """

    """

    global resumo_produto
    parametros = Parametro.objects.get(empresa_id=id_empresa)
    fornecedor = Fornecedor.objects.get(cod_fornecedor=cod_fornecedor, empresa__id__exact=id_empresa)

    # ja ajustados
    pedidos = pedidos_compra(cod_produto=cod_produto, id_empresa=id_empresa)
    u_entrada = ultima_entrada(cod_produto=cod_produto, id_empresa=id_empresa, periodo=periodo)
    e_atual = estoque_atual(cod_produto=cod_produto, id_empresa=id_empresa)

    vendas_p, info_produto = vendas(cod_produto, id_empresa, periodo)

    lista_resumo = []
    lista_fornecedor = [cod_fornecedor]

    if not curva_home:
        curva = abc_fornecedores(lista_fornecedor, id_empresa, periodo)
    else:
        curva = curva_filial

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

        curva_ = curva.query('cod_produto == @cod_produto & cod_filial == @filial').reset_index(drop=True)

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
        temp_est = fornecedor.tempo_estoque

        prod_resumo['sugestao'] = sugestao
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
        est_disponivel = prod_resumo['estoque_dispon'].unique()

        # Função responsável pela classificação da condição de estoque
        results_condicao_estoque = define_condicao_estoque(produto_resumo=prod_resumo,
                                                           tempo_reposicao=temp_est,
                                                           dde=dde, media=media,
                                                           estoque_disponivel=est_disponivel,
                                                           dde_ponto_reposicao=dde_ponto_rep,
                                                           preco_custo=preco_custo
                                                           )

        lista_resumo.append(results_condicao_estoque)

        lista_fim = []
        for a in lista_resumo:
            for b in a:
                lista_fim.append(b)
        resumo_produto = pd.DataFrame(lista_fim)

    return resumo_produto


def processa_produtos_alerta_home(id_empresa, periodo, curva_filial, curva_home):
    global alertas_produtos, infor_filiais, condicao

    lista_alertas = []

    fornecedores = get_fornecedores_qs(id_empresa)

    for fornecedor in fornecedores:

        leadtime = fornecedor.leadtime
        t_reposicao = fornecedor.ciclo_reposicao

        produtos = get_produtos(id_empresa, fornecedor.id)

        for produto in produtos:
            verif_produto = verifica_produto(produto.cod_produto, id_empresa, periodo)

            if verif_produto:
                infor_filiais = processa_produtos_filiais(
                    produto.cod_produto,
                    fornecedor.cod_fornecedor,
                    id_empresa,
                    leadtime,
                    t_reposicao,
                    periodo,
                    curva_filial,
                    curva_home
                )

                infor_filiais['cod_produto'] = produto.cod_produto
                infor_filiais['desc_produto'] = produto.desc_produto
                infor_filiais['principio_ativo'] = produto.principio_ativo
                infor_filiais['fornecedor'] = fornecedor.desc_fornecedor
                infor_filiais['cod_fornecedor'] = fornecedor.cod_fornecedor

                for index, row in infor_filiais.iterrows():
                    alertas_produtos = {
                        'filial': row.filial,
                        'cod_produto': row.cod_produto,
                        'desc_produto': row.desc_produto,
                        'saldo': row.saldo,
                        'sugestao_unidade': row.sugestao,
                        'valor_sugestao': row.valor_sugestao,
                        'condicao_estoque': row.condicao_estoque,
                        'estoque': row.estoque,
                        'qt_excesso': row.qt_excesso,
                        'vl_excesso': row.vl_excesso,
                        'curva': row.curva,
                        'custo': row.custo,
                        'fornecedor': row.fornecedor,
                        'cod_fornecedor': row.cod_fornecedor,
                        'dde': row.dde,
                        'quantidade_calc': row.quantidade_calc,
                        # 'media_ajustada': row.media_ajustada,
                        'media': row.media_simples,
                        'principio_ativo': row.principio_ativo,
                        'dt_ult_entrada': row.dt_ult_entrada,
                        'vl_ult_entrada': row.vl_ult_entrada,
                    }

                    lista_alertas.append(alertas_produtos)
    return lista_alertas
