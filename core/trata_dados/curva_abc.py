from api.models.venda import Venda
import pandas as pd
import datetime
from core.models.parametros_models import Parametro
from core.multifilial.filiais import get_filiais
from core.trata_dados.datas import dia_semana_mes_ano
from core.models.empresas_models import Filial

def curva_abc(cod_fornecedor, id_empresa, periodo):
    global lista_fim
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    filiais = get_filiais(id_empresa)

    list = []
    for filial in filiais:
        vendas_df = pd.DataFrame(Venda.objects.filter(
            cod_fornecedor__in=cod_fornecedor,
            cod_filial__exact=filial.cod_filial,
            data__range=[data_fim, data_inicio],
            empresa__id__exact=id_empresa
        ).values())
        if not vendas_df.empty:
            vendas_ = vendas_df
            lista = vendas_.values.tolist()
            list.append(lista)

    list_curva = []

    if len(list) != 0:
        for i in list:
            df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial", "cod_fornecedor", "qt_vendas", "preco_unit",
                                              "custo_fin", "data", "cliente", "num_nota", "cod_usur", "supervisor", "created_at",
                                              "produto_id", "fornecedor_id", "filial_id", "empresa_id", "campo_um", "campo_dois", "campo_tres"])

            df.drop(columns=["campo_um", "campo_dois", "campo_tres"], inplace=True)

            df['qt_vendas'].fillna(0, inplace=True)

            df['vl_total_vendido'] = df['qt_vendas'] * df['preco_unit']
            df['vl_total_custo'] = df['qt_vendas'] * df['custo_fin']

            vendas_df_abc = df
            list_val_cus = ['vl_total_vendido', 'vl_total_custo']
            abc = vendas_df_abc.groupby(['cod_produto'])[list_val_cus].sum().round(2).reset_index()
            abc['cod_filial'] = df['cod_filial']
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

            if not abc.empty:
                curva = abc.assign(
                    **abc.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

            list_curva.append(curva)

            lista_fim = []
            for a in list_curva:
                for b in a:
                    lista_fim.append(b)

        curva_abc = pd.DataFrame(lista_fim)

        return curva_abc
    else:
        vazio = pd.DataFrame()
        return vazio
