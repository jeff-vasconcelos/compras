from api.models.vendas_models import Venda
import pandas as pd
import datetime

from core.trata_dados.datas import dia_semana_mes_ano


def abc(cod_fornecedor, id_empresa, periodo):
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1
    datas = dia_semana_mes_ano(id_empresa)


    vendas_df = pd.DataFrame(Venda.objects.filter(
        cod_fornecedor=cod_fornecedor,
        empresa__id__exact=id_empresa,
        data__range=[data_fim, data_inicio]
    ).values())

    if not vendas_df.empty:
        vendas_df['vl_total_vendido'] = vendas_df['qt_vendas'] * vendas_df['preco_unit']
        vendas_df['vl_total_custo'] = vendas_df['qt_vendas'] * vendas_df['custo_fin']

        vendas_df_abc = vendas_df
        list_val_cus = ['vl_total_vendido', 'vl_total_custo']
        abc = vendas_df_abc.groupby(['cod_produto'])[list_val_cus].sum().round(2).reset_index()
        abc['lucro'] = abc['vl_total_vendido'] - abc['vl_total_custo']
        abc.sort_values(by='lucro', ascending=False, inplace=True)

        lucro_total = abc['lucro'].sum().round(2)

        lista_participacao = []

        for i in abc.lucro:
            participacao = i / lucro_total

            lista_participacao.append(participacao)

        abc['share'] = lista_participacao

        lista_share = []
        soma = 0
        for i in abc.share:
            soma = i + soma
            lista_share.append(soma)

        abc['share_total'] = lista_share

        lista_curva = []
        curva = ""
        for i in abc.share_total:
            if i <= 0.70:
                curva = "A"
            elif i <= 0.85:
                curva = "B"
            elif i <= 0.95:
                curva = "C"
            elif i <= 0.99:
                curva = "D"
            else:
                curva = "E"

            lista_curva.append(curva)
        abc['curva'] = lista_curva

        print("CURVA ABC - ABC OK")
        print("##############################")

        return abc
    else:
        return None