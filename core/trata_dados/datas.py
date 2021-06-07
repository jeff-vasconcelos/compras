import pandas as pd
import datetime
from core.models.parametros_models import Parametro


def validando_mes(mes):
    nome_mes = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
    m = mes - 1
    mes_valido = nome_mes[m]

    return mes_valido


def daterange(start_date, end_date, periodo):

    data = datetime.date.today() + datetime.timedelta(days=1)
    start_date = datetime.date.today() - datetime.timedelta(days=periodo - 1) #Aqui sempre será o periodo informado -1
    end_date = data

    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def dia_semana_mes_ano(id_empresa):
    parametros = Parametro.objects.get(empresa_id=id_empresa)
    periodo = parametros.periodo
    data = datetime.date.today() + datetime.timedelta(days=1)
    start_date = datetime.date.today() - datetime.timedelta(days=periodo - 1) #Aqui sempre será o periodo informado -1
    end_date = data

    nome_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"]

    disc = {}
    lista_data = []
    lista_semana = []
    lista_mes = []
    lista_ano = []

    for single_date in daterange(start_date, end_date, periodo):
        wk_num = int(single_date.strftime("%w"))
        ms_num = int(single_date.strftime("%m"))
        an_num = int(single_date.strftime("%Y"))

        mes = validando_mes(ms_num)

        lista_data.append(single_date)
        lista_semana.append(nome_semana[wk_num])
        lista_mes.append(mes)
        lista_ano.append(an_num)

    disc['data'] = lista_data
    disc['semana'] = lista_semana
    disc['mes'] = lista_mes
    disc['ano'] = lista_ano

    datas = pd.DataFrame(data=disc)
    datas.sort_values(by='data', ascending=False, inplace=True)
    datas['data'] = pd.to_datetime(datas['data'])

    return datas
