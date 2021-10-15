import locale
import pandas as pd
import datetime
from api.models.venda import Venda
from core.models.empresas_models import Empresa
from core.models.parametros_models import GraficoCurva, DadosEstoque, GraficoFaturamento, Parametro
from core.views.alerta.verificador import get_filiais
from core.views.utils.functions_calc import calcula_curva

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


# TODO (status: Validando)
def save_grafico_curva(id_empresa, produtos):
    """ Função responsável por salvar no DB os totais por curva e condição de estoque"""

    graf_curva = GraficoCurva.objects.all().filter(empresa__id__exact=id_empresa)
    empresa = Empresa.objects.get(id=id_empresa)
    results = total_por_condicao_e_curva(produtos)  # dataframe

    # Remove registros existentes no DB
    if graf_curva:
        graf_curva.delete()

    if not 'NORMAL' in results.columns:
        results['NORMAL'] = 0
    if not 'EXCESSO' in results.columns:
        results['EXCESSO'] = 0
    if not 'PARCIAL' in results.columns:
        results['PARCIAL'] = 0

    for index, row in results.iterrows():
        normal = row['NORMAL']
        excesso = row['EXCESSO']
        parcial = row['PARCIAL']

        total = (normal + excesso + parcial)

        # Gravando no DB
        c = GraficoCurva.objects.create(
            curva=row['curva'],
            normal=round(normal, 2),
            parcial=round(parcial, 2),
            excesso=round(excesso, 2),
            total=round(total, 2),
            empresa=empresa
        )
        c.save()


def total_por_condicao_e_curva(produtos):
    """
        Função realiza os calculos usando pandas para alcançar os valores totais, considerando
        a curva e a condição do estoque
    """

    df = pd.DataFrame(data=produtos)
    df['valor'] = df['quantidade_calc'] * df['custo']
    results = df.groupby(['curva', 'condicao_estoque'])['valor'].sum().round(2).to_frame().reset_index()
    results = pd.pivot_table(results, values='valor', index='curva', columns='condicao_estoque').reset_index()
    results = results.fillna(0)

    return results


# TODO (Status: Validando)
def save_grafico_faturamento(id_empresa):
    """ Função responsável por salvar no DB o total de faturamento por curva """

    empresa = Empresa.objects.get(id=id_empresa)
    parametros = Parametro.objects.get(empresa_id=id_empresa)
    graf_fat = GraficoFaturamento.objects.all().filter(empresa__id__exact=id_empresa)
    curva_df = abc_home(id_empresa, parametros.periodo)  # dataframe

    curva = curva_df.groupby(['curva'])['vl_total_vendido'].sum().round(2).to_frame().reset_index()

    valor_total = curva['vl_total_vendido'].sum()
    curva['porcentagem'] = round(curva['vl_total_vendido'] * 100 / valor_total, 2)

    # Remove registros existentes no DB
    if graf_fat:
        graf_fat.delete()

    # Gravando no DB
    for index, row in curva.iterrows():
        f = GraficoFaturamento.objects.create(
            curva=row['curva'],
            total=row['vl_total_vendido'],
            # parcticipacao=row['porcentagem'],
            empresa=empresa
        )
        f.save()


# TODO (Status: Validando)
def save_dados_estoque(id_empresa, produtos):
    """ Função responsável por salvar no DB o total de SKU's por curva e condição de estoque """

    dados_est = DadosEstoque.objects.all().filter(empresa__id__exact=id_empresa)
    empresa = Empresa.objects.get(id=id_empresa)
    results = total_sku_por_condicao_e_curva(produtos)  # dataframe

    # Remove registros existentes no DB
    if dados_est:
        dados_est.delete()

    if not 'NORMAL' in results.columns:
        results['NORMAL'] = 0
    if not 'EXCESSO' in results.columns:
        results['EXCESSO'] = 0
    if not 'PARCIAL' in results.columns:
        results['PARCIAL'] = 0
    if not 'RUPTURA' in results.columns:
        results['RUPTURA'] = 0

    results['skus'] = results['RUPTURA'] + results['PARCIAL'] + results['EXCESSO'] + results['NORMAL']

    for index, row in results.iterrows():
        # Gravando no DB
        b = DadosEstoque.objects.create(
            curva=row['curva'],
            skus=row['skus'],
            normal=row['NORMAL'],
            parcial=row['PARCIAL'],
            excesso=row['EXCESSO'],
            ruptura=row['RUPTURA'],
            empresa=empresa
        )
        b.save()


def total_sku_por_condicao_e_curva(produtos):
    """
        Função realiza os calculos usando pandas para alcançar os quantidade total de SKU's, considerando
        a curva e a condição do estoque
    """

    df = pd.DataFrame(data=produtos)
    results = df.groupby(['curva', 'condicao_estoque']).size().reset_index(name='skus')
    results = pd.pivot_table(results, values='skus', index='curva', columns='condicao_estoque').reset_index()
    results = results.fillna(0)

    return results


def abc_home(id_empresa, periodo):
    """
        Função consulta o DB na tabela de vendas e realiza calculos de curva ABC desconsiderando fornecedores
    """

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
