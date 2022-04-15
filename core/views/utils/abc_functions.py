import pandas as pd
import datetime

from api.models.venda import Venda
from core.views.alerta.verificador import get_filiais

# TODO TRABLHANDO NESTA CLASS 15/10
from core.views.utils.datas import intervalo_periodo


def abc_home(id_empresa, periodo):
    """
        Função consulta o DB na tabela de vendas e realiza calculos de curva ABC desconsiderando fornecedores
    """

    inicio, fim = intervalo_periodo(periodo)

    filiais = get_filiais(id_empresa)

    lista_vendas = []

    for filial in filiais:
        vendas_df = pd.DataFrame(Venda.objects.filter(
            cod_filial__exact=filial.cod_filial,
            data__range=[fim, inicio],
            empresa__id__exact=id_empresa
        ).values())

        if not vendas_df.empty:
            vendas_ = vendas_df
            lista = vendas_.values.tolist()
            lista_vendas.append(lista)

    results = calcula_curva(lista_vendas)

    return results


def abc_fornecedores(lista_fornecedores, id_empresa, periodo):
    """
        Função consulta o DB na tabela de vendas e realiza calculos de curva ABC considerando fornecedores
    """

    inicio, fim = intervalo_periodo(periodo)
    filiais = get_filiais(id_empresa)

    lista_vendas = []


    for filial in filiais:
        vendas_df = pd.DataFrame(Venda.objects.filter(
            cod_fornecedor__in=lista_fornecedores,
            cod_filial__exact=filial.cod_filial,
            data__range=[fim, inicio],
            empresa__id__exact=id_empresa
        ).values())

        if not vendas_df.empty:
            vendas_ = vendas_df
            lista = vendas_.values.tolist()
            lista_vendas.append(lista)

    results = calcula_curva(lista_vendas)

    return results


def calcula_curva(lista_vendas):
    """ Função responsável por calcular curva abc """

    list_curva = []
    lista_fim = []

    for i in lista_vendas:
        df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial", "cod_fornecedor", "qt_vendas", "preco_unit",
                                      "custo_fin", "data", "cliente", "num_nota", "cod_usur", "supervisor",
                                      "created_at", "updated_at", "produto_id", "fornecedor_id", "filial_id", "empresa_id",
                                      "campo_um", "campo_dois", "campo_tres"])

        df.drop(columns=["campo_um", "campo_dois", "campo_tres"], inplace=True)

        df['qt_vendas'].fillna(0, inplace=True)

        df['vl_total_vendido'] = df['qt_vendas'] * df['preco_unit']
        df['vl_total_custo'] = df['qt_vendas'] * df['custo_fin']

        df_vendas_abc = df
        list_val_cus = ['vl_total_vendido', 'vl_total_custo']
        abc = df_vendas_abc.groupby(['cod_produto'])[list_val_cus].sum().round(2).reset_index()
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

        for a in list_curva:
            for b in a:
                lista_fim.append(b)

    curva_abc = pd.DataFrame(lista_fim)

    return curva_abc
