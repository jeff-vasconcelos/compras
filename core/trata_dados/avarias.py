from api.models.avarias_models import Avaria
import pandas as pd
import datetime


def avarias(cod_produto, id_empresa, periodo):

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1) #Aqui sempre será o periodo informado -1

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    avarias_df = pd.DataFrame(Avaria.objects.filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa,
        data__range=[data_fim, data_inicio]
    ).values())

    if not avarias_df.empty:
        avarias = avarias_df.groupby(['data', 'cod_produto', 'desc_produto', 'cod_filial'])['qt_avaria'].sum().to_frame().reset_index()
        avarias['data'] = pd.to_datetime(avarias['data'])

        print("AVARIAS - AVARIAS DO PRODUTO NO PERIODO")
        print("##############################")

        return avarias
    else:
        print("AVARIAS - O PRODUTO NÃO PUSSUI AVARIAS NO PERIODO")
        print("##############################")

        return None