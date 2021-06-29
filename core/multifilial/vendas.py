from api.models.venda import Venda
from core.models.parametros_models import Parametro
from core.models.empresas_models import Filial
from core.trata_dados.datas import dia_semana_mes_ano
import pandas as pd
import datetime


def vendas(cod_produto, id_empresa, periodo):
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1
    datas = dia_semana_mes_ano(id_empresa)

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    vendas_df = pd.DataFrame(Venda.objects.filter(
        cod_produto__exact=cod_produto,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=id_empresa
    ).values())

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    if not vendas_df.empty:

        list = []
        for filial in filiais:
            vendas_ = vendas_df
            vendas_ = vendas_.query('cod_filial == @filial.cod_filial')
            lista = vendas_.values.tolist()
            list.append(lista)


        list_vendas = []
        lista_fim_vendas = []
        lista_prod = []
        list_inf_prod = []

        for i in list:
            if i:
                df = pd.DataFrame(i, columns=["id", "cod_produto", "desc_produto", "cod_filial", "filial_id",
                                              "cod_fornecedor", "produto_id", "fornecedor_id", "empresa_id", "qt_vendas",
                                              "qt_unit_caixa", "preco_unit", "custo_fin", "data", "cliente", "marca",
                                              "peso_liquido", "cod_depto", "num_nota", "cod_usur", "cod_fab", "desc_dois",
                                              "supervisor", "created_at"])
                vendas_df = df
                vendas_df['data'] = pd.to_datetime(vendas_df['data'])

                preco = vendas_df.groupby(['data'])['preco_unit'].mean().round(2).to_frame().reset_index()
                media_preco_vendas = preco['preco_unit'].mean(skipna=True)
                custo = vendas_df.groupby(['data'])['custo_fin'].mean().round(2).to_frame().reset_index()

                preco_custo = pd.merge(preco, custo, how="left", on=["data"])

                qtvendas = \
                    vendas_df.groupby(
                        ['data', 'cod_produto', 'desc_produto', 'cod_filial', 'cod_fornecedor', 'qt_unit_caixa'])[
                        'qt_vendas'].sum().to_frame().reset_index()

                qtvendas_preco_custo = pd.merge(qtvendas, preco_custo, how="left", on=["data"])

                vendas_datas = pd.merge(datas, qtvendas_preco_custo, how="left", on=["data"])

                cod_filial = vendas_datas['cod_filial'].unique()
                cod_prod = vendas_datas['cod_produto'].unique()
                cod_fornec = vendas_datas['cod_fornecedor'].unique()
                desc_prod = vendas_datas['desc_produto'].unique()
                qt_un_caixa = vendas_datas['qt_unit_caixa'].unique()

                if vendas_df.size == 1:
                    values = {'cod_produto': cod_prod[0], 'desc_produto': desc_prod[0], 'cod_filial': cod_filial[0],
                              'cod_fornecedor': cod_fornec[0], 'qt_unit_caixa': qt_un_caixa[0], 'qt_vendas': 0,
                              'custo_fin': 0,
                              'preco_unit': 0}
                else:
                    values = {'cod_produto': cod_prod[1], 'desc_produto': desc_prod[1], 'cod_filial': cod_filial[1],
                              'cod_fornecedor': cod_fornec[1], 'qt_unit_caixa': qt_un_caixa[1], 'qt_vendas': 0,
                              'custo_fin': 0,
                              'preco_unit': 0}

                vendas_datas.fillna(value=values, inplace=True)

                # ESTATISTICAS DE VENDAS

                e_vendas = vendas_datas
                tratando_media = e_vendas['qt_vendas'].apply(lambda x: 0 if x <= 0 else x)
                media = tratando_media.mean()

                maximo = e_vendas['qt_vendas'].max()
                d_padrao = tratando_media.std()

                d_vendas = e_vendas['qt_vendas'].apply(lambda x: 0 if x <= 0 else 1).sum()
                d_sem_vendas = 120 - d_vendas

                d_m = d_padrao / media
                d_m_dois = d_m * 2
                d_m_media = media * d_m_dois
                max_media = d_m_media + media

                # CONSIDERAR VENDAS MAIORES OU IGUAIS A ZERO E MENORES QUE A MÉDIA MAXIMA
                lista_media = []
                for i in e_vendas.qt_vendas:
                    if i < max_media and i >= 0:
                        lista_media.append(i)
                lista_for_df = pd.DataFrame(data=lista_media, columns=["valores"]).reset_index()
                media_ajustada = lista_for_df['valores'].mean()

                # ADICIONANDO VALORES AO DATAFRAME
                e_vendas['media'] = media.round(2)
                e_vendas['max'] = round(max_media, 2)
                e_vendas['min'] = 0

                # VALIDANDO VENDAS FORA DA MEDIA
                lista_fora = []
                for i in e_vendas.qt_vendas:
                    if i > max_media:
                        item = round(i)
                    else:
                        item = 0
                    lista_fora.append(item)

                e_vendas['fora_media'] = lista_fora

                info_p = {
                    'cod_filial': e_vendas.cod_filial[0],
                    'dias_s_vendas': [d_sem_vendas], 'dias_vendas': [d_vendas],
                    'media': [media.round(2)], 'maximo': [maximo], 'desvio': [d_padrao.round(2)],
                    'max_media': [max_media.round(2)],
                    'media_ajustada': [media_ajustada.round(2)],
                    'qt_unit_caixa': e_vendas['qt_unit_caixa'][0],
                    'media_preco_praticado': media_preco_vendas
                }
                info_prod = pd.DataFrame(info_p)

                list_val_cus = ['vl_total_vendido', 'vl_total_custo']
                vendas_lucro = e_vendas

                vendas_lucro['vl_total_vendido'] = e_vendas['qt_vendas'] * e_vendas['preco_unit']
                vendas_lucro['vl_total_custo'] = e_vendas['qt_vendas'] * e_vendas['custo_fin']

                lucro = vendas_lucro.groupby(['data'])[list_val_cus].sum().round(2).reset_index()
                e_vendas['lucro'] = vendas_lucro['vl_total_vendido'] - vendas_lucro['vl_total_custo']

                # VENDAS
                _venda = e_vendas
                _vendas = _venda.assign(
                    **_venda.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

                list_vendas.append(_vendas)

                for a in list_vendas:
                    for b in a:
                        lista_fim_vendas.append(b)

                vendas = pd.DataFrame(lista_fim_vendas)

                # INFOR PRODUTO
                _info = info_prod
                _info = _info.to_dict('records')

                list_inf_prod.append(_info)

                for c in list_inf_prod:
                    for d in c:
                        lista_prod.append(d)
                    # print(lista_prod)

                informacao_produto = pd.DataFrame(lista_prod)
            informacao_produto = informacao_produto.drop_duplicates(subset=['cod_filial'], keep='first')
            vendas = vendas.drop_duplicates(subset=['data', 'cod_produto', 'cod_filial'], keep='first')

        return vendas, informacao_produto

    if vendas_df.empty:
        print("VENDAS - NÃO HÁ VENDAS")
        print("##############################")

        return None, None