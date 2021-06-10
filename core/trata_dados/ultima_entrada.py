from api.models.ultima_entrada_models import UltimaEntrada
import pandas as pd
import datetime


def ultima_entrada(cod_produto, id_empresa, periodo):
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    u_entrada_df = pd.DataFrame(UltimaEntrada.objects.filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa,
        data__range=[data_fim, data_inicio]
    )[:1].values())

    if not u_entrada_df.empty:
        data = u_entrada_df['data'][0]
        qt_entrada = u_entrada_df['qt_ult_entrada'][0]
        vl_entrada = u_entrada_df['vl_ult_entrada'][0]

        entr = {
            'data': [data], 'qt_ult_entrada': [qt_entrada], 'vl_ult_entrada': [vl_entrada]
        }

        entrada = pd.DataFrame(entr)

        print("ENTRADAS - OK")
        print("##############################")

        return entrada
    else:
        print("ENTRADAS - O PRODUTO NÃO TEM ENTRADAS")
        print("##############################")

        return None