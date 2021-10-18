import numpy

from api.models.venda import Venda
from core.views.alerta.historico import historico_estoque
from api.models.produto import Produto
from core.views.alerta.verificador import get_filiais
from core.views.utils.datas import dia_semana_mes_ano
import pandas as pd
import datetime


def vendas(cod_produto, id_empresa, periodo):
    global vendas, informacao_produto, produto_qs, filial_cod, duplicados
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1
    datas = dia_semana_mes_ano(id_empresa)

    filiais = get_filiais(id_empresa)

    list = []
    for filial in filiais:

        vendas_df = pd.DataFrame(Venda.objects.filter(
            cod_produto__exact=cod_produto,
            cod_filial__exact=filial.cod_filial,
            data__range=[data_fim, data_inicio],
            empresa__id__exact=id_empresa
        ).values())

        produto_qs = Produto.objects.get(
            cod_produto__exact=cod_produto,
            empresa__id__exact=id_empresa
        )

        if not vendas_df.empty:
            vendas_ = vendas_df
            lista = vendas_.values.tolist()
            list.append(lista)

    list_vendas = []
    lista_fim_vendas = []
    lista_prod = []
    list_inf_prod = []

    for i in list:
        if i:
            df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial", "cod_fornecedor", "qt_vendas", "preco_unit",
                                          "custo_fin", "data", "cliente", "num_nota", "cod_usur", "supervisor", "created_at",
                                          "produto_id", "fornecedor_id", "filial_id", "empresa_id", "campo_um", "campo_dois",
                                          "campo_tres"
                                          ])

            df.drop(columns=['campo_um', 'campo_dois', 'campo_tres'], inplace=True)

            vendas_df = df

            vendas_df['data'] = pd.to_datetime(vendas_df['data'])

            preco = vendas_df.groupby(['data'])['preco_unit'].mean().round(2).to_frame().reset_index()
            media_preco_vendas = preco['preco_unit'].mean(skipna=True)
            custo = vendas_df.groupby(['data'])['custo_fin'].mean().round(2).to_frame().reset_index()

            preco_custo = pd.merge(preco, custo, how="left", on=["data"])

            qtvendas = \
                vendas_df.groupby(
                    ['data', 'cod_produto', 'cod_filial', 'cod_fornecedor'])[
                    'qt_vendas'].sum().to_frame().reset_index()

            qtvendas_preco_custo = pd.merge(qtvendas, preco_custo, how="left", on=["data"])

            #MERGE VENDAS X DATAS
            vendas_datas = pd.merge(datas, qtvendas_preco_custo, how="left", on=["data"])

            vendas_datas = vendas_datas.drop_duplicates(subset=['data', 'cod_produto', 'cod_filial'], keep='first')


            cod_filial = vendas_datas['cod_filial'].unique()
            cod_filial = cod_filial[~numpy.isnan(cod_filial)]

            for f in cod_filial:
                filial_cod = f

            values = {'cod_produto': produto_qs.cod_produto, 'cod_filial': filial_cod,
                      'cod_fornecedor': produto_qs.cod_fornecedor, 'qt_vendas': 0,
                      'custo_fin': 0,
                      'preco_unit': 0,
                      'quantidade_un_caixa': produto_qs.quantidade_un_cx
                      }

            vendas_datas.fillna(value=values, inplace=True)

            # MERGE VENDAS X HISTORICO
            df_historico = historico_estoque(cod_produto, id_empresa, periodo)
            df_historico['data'] = pd.to_datetime(df_historico['data'])

            vendas_dt = pd.merge(vendas_datas, df_historico, how="left",
                                    on=["data", "cod_produto", "cod_filial"])

            e_vendas = vendas_dt
            tratando_media = e_vendas['qt_vendas'].apply(lambda x: 0 if x <= 0 else x)


            maximo = e_vendas['qt_vendas'].max()
            d_padrao = tratando_media.std()

            d_vendas = e_vendas['qt_vendas'].apply(lambda x: 0 if x <= 0 else 1).sum()
            d_sem_vendas = periodo - d_vendas


            values = {'qt_estoque': 0}
            e_vendas.fillna(value=values, inplace=True)
            e_vendas.drop(
                columns=['id', 'produto_id', 'fornecedor_id', 'empresa_id', 'created_at', 'cod_fornecedor_y',
                         'filial_id'],
                inplace=True)

            lista_media = []
            for v, est in zip(e_vendas.qt_vendas, e_vendas.qt_estoque):
                if est > 0:
                    lista_media.append(v)

            lista_for_df = pd.DataFrame(data=lista_media, columns=["valores"]).reset_index()

            media = lista_for_df['valores'].mean()


            if media == 0:
                media = 0.1

            d_m = d_padrao / media
            d_m_dois = d_m * 2
            d_m_media = media * d_m_dois
            max_media = d_m_media + media


            # ADICIONANDO VALORES AO DATAFRAME
            e_vendas['media'] = media
            e_vendas['max'] = round(max_media, 2)
            e_vendas['min'] = 0

            # VALIDANDO VENDAS FORA DA MEDIA
            lista_fora = []
            for z in e_vendas.qt_vendas:
                if z > max_media:
                    item = round(z)
                else:
                    item = 0
                lista_fora.append(item)

            e_vendas['fora_media'] = lista_fora

            info_p = {
                'cod_filial': filial_cod,
                'dias_s_vendas': [d_sem_vendas], 'dias_vendas': [d_vendas],
                'media': [media], 'maximo': [maximo], 'desvio': [d_padrao.round(2)],
                'max_media': [max_media.round(2)],
                'embalagem': produto_qs.embalagem,
                #'media_ajustada': [round(media_ajustada, 2)],
                'quantidade_un_caixa': produto_qs.quantidade_un_cx,
                'media_preco_praticado': media_preco_vendas
            }
            info_prod = pd.DataFrame(info_p)

            list_val_cus = ['vl_total_vendido', 'vl_total_custo']
            vendas_lucro = e_vendas

            vendas_lucro['vl_total_vendido'] = e_vendas['qt_vendas'] * e_vendas['preco_unit']
            vendas_lucro['vl_total_custo'] = e_vendas['qt_vendas'] * e_vendas['custo_fin']

            lucro = vendas_lucro.groupby(['data'])[list_val_cus].sum().round(2).reset_index()
            e_vendas['lucro'] = vendas_lucro['vl_total_vendido'] - vendas_lucro['vl_total_custo']
            e_vendas['embalagem'] = produto_qs.embalagem

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

            informacao_produto = pd.DataFrame(lista_prod)
            duplicados = vendas[vendas.duplicated(keep='first')]

        if not duplicados.empty:
            informacao_produto = informacao_produto.drop_duplicates(subset=['cod_filial'], keep='first')
            vendas = vendas.drop_duplicates(subset=['data', 'cod_produto', 'cod_filial'], keep='first')

    return vendas, informacao_produto
