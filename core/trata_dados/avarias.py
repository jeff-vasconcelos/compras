from api.models.avarias_models import Avaria
import pandas as pd
import datetime


def avarias():

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=119) #Aqui sempre será o periodo informado -1

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    avarias_df = pd.DataFrame(Avaria.objects.filter(
        cod_produto__exact=183,
        empresa__id__exact=1,
        data__range=[data_fim, data_inicio]
    ).values())

    if not avarias_df.empty:
        avarias = avarias_df.groupby(['data', 'cod_produto', 'desc_produto', 'cod_filial'])['qt_avaria'].sum().to_frame().reset_index()
        avarias['data'] = pd.to_datetime(avarias['data'])
        return avarias
    else:
        print("O produto não possui avarias no periodo!")
        return None