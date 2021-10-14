import locale
import pandas as pd
import datetime
from core.models.empresas_models import Empresa
from core.models.parametros_models import GraficoCurva, DadosEstoque, GraficoFaturamento, Parametro
from api.models.venda import Venda
from core.views.alerta.verificador import get_filiais
from core.views.utils.functions_calc import calcula_curva

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def save_grafico_curva(id_empresa, produtos):
    """ fu """
    graf_curva = GraficoCurva.objects.all().filter(empresa__id__exact=id_empresa)
    empresa = Empresa.objects.get(id=id_empresa)
    results = total_por_condicao_e_curva(produtos) #dataframe

    if graf_curva:
        graf_curva.delete()

    for i in results:
        normal = i['total_normal']
        excesso = i['total_excesso']
        parcial = i['total_parcial']
        total = normal + excesso + parcial

        c = GraficoCurva.objects.create(
            curva=i['curva'],
            normal=round(normal, 2),
            parcial=round(parcial, 2),
            excesso=round(excesso, 2),
            total=round(total, 2),
            empresa=empresa
        )

        c.save()


def save_grafico_faturamento(id_empresa):
    empresa = Empresa.objects.get(id=id_empresa)
    parametros = Parametro.objects.get(empresa_id=id_empresa)
    graf_fat = GraficoFaturamento.objects.all().filter(empresa__id__exact=id_empresa)
    curva = abc_home(id_empresa, parametros.periodo) #dataframe

    curva = curva.groupby(['curva'])['vl_total_vendido'].sum().round(2).to_frame().reset_index()

    if graf_fat:
        graf_fat.delete()

    for index, row in curva.iterrows():
        f = GraficoFaturamento.objects.create(
            curva=row['curva'],
            total=row['total'],
            empresa=empresa
        )
        f.save()


def save_dados_estoque(id_empresa, produtos):
    dados_est = DadosEstoque.objects.all().filter(empresa__id__exact=id_empresa)
    empresa = Empresa.objects.get(id=id_empresa)
    results = total_sku_por_condicao_e_curva(produtos)  # dataframe

    if dados_est:
        dados_est.delete()

    for index, row in results.iterrows():
        b = DadosEstoque.objects.create(
            curva=row['curva'],
            skus=row['skus'],
            normal=row['normal'],
            parcial=row['parcial'],
            excesso=row['excesso'],
            ruptura=row['ruptura'],
            empresa=empresa
        )
        b.save()


def total_por_condicao_e_curva(produtos):
    df = pd.DataFrame(data=produtos)
    df['total'] = df['estoque_disp'] * df['custo_fin']
    results = df.groupby(['condicao_est', 'curva'])['total'].sum().round(2).to_frame().reset_index()

    return results


def total_sku_por_condicao_e_curva(produtos):
    df = pd.DataFrame(data=produtos)
    df['contador'] = 1
    results = df.groupby(['curva', 'condicao'])['contador'].sum().round(2).to_frame().reset_index()

    return results


def abc_home(id_empresa, periodo):
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)

    filiais = get_filiais(id_empresa)

    lista_vendas = []

    for filial in filiais:
        vendas_df = pd.DataFrame(Venda.objects.filter(
            cod_filial__exact=filial.cod_filial,
            data__range=[data_fim, data_inicio],
            empresa__id__exact=id_empresa
        ).values())

        if not vendas_df.empty:
            vendas_ = vendas_df
            lista = vendas_.values.tolist()
            lista_vendas.append(lista)

    results = calcula_curva(lista_vendas)

    return results


