from api.models.vendas_models import Venda
from core.trata_dados.datas import dia_semana_mes_ano
import pandas as pd
import datetime


def vendas():
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=119) #Aqui sempre será o periodo informado -1
    datas = dia_semana_mes_ano()

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    vendas_df = pd.DataFrame(Venda.objects.filter(
        cod_produto__exact=182,
        empresa__id__exact=1,
        data__range=[data_fim, data_inicio]
    ).values())

    if not vendas_df.empty:
        #TRATANDO DADOS
        vendas_df['data'] = pd.to_datetime(vendas_df['data'])
        preco = vendas_df.groupby(['data'])['preco_unit'].mean().round(2).to_frame().reset_index()
        custo = vendas_df.groupby(['data'])['custo_fin'].mean().round(2).to_frame().reset_index()

        preco_custo = pd.merge(preco, custo, how="left", on=["data"])

        qtvendas = vendas_df.groupby(['data', 'cod_produto', 'desc_produto', 'cod_filial', 'cod_fornecedor', 'qt_unit_caixa'])['qt_vendas'].sum().to_frame().reset_index()

        qtvendas_preco_custo = pd.merge(qtvendas, preco_custo, how="left", on=["data"])
        vendas_datas = pd.merge(datas, qtvendas_preco_custo, how="left", on=["data"])

        cod_filial = vendas_datas['cod_filial'].unique()
        cod_prod = vendas_datas['cod_produto'].unique()
        cod_fornec = vendas_datas['cod_fornecedor'].unique()
        desc_prod = vendas_datas['desc_produto'].unique()

        values = {'cod_produto': cod_prod[0], 'desc_produto': desc_prod[0], 'cod_filial': cod_filial[0],
                  'cod_fornecedor': cod_fornec[0], 'qt_vendas': 0, 'custo_fin': 0, 'preco_unit': 0}

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
        e_vendas['media'] = round(media, 2)
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
            'dias_s_vendas': [d_sem_vendas], 'dias_vendas': [d_vendas],
            'media': [round(media, 2)], 'maximo': [maximo], 'desvio': [round(d_padrao, 2)],
            'max_media': [round(max_media, 2)],
            'media_ajustada': [round(media_ajustada, 2)]
        }
        info_prod = pd.DataFrame(info_p)

        return e_vendas, info_prod

    if vendas_df.empty:
        return None
