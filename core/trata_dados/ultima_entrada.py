from api.models.ultima_entrada_models import UltimaEntrada
import pandas as pd
import datetime


def ultima_entrada():
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=119)  # Aqui sempre será o periodo informado -1

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    u_entrada_df = pd.DataFrame(UltimaEntrada.objects.filter(
        cod_produto__exact=2042,
        empresa__id__exact=2,
        data__range=[data_fim, data_inicio]
    )[:1].values())

    if not u_entrada_df.empty:
        data = u_entrada_df['data'][0]
        qt_entrada = u_entrada_df['qt_ult_entrada'][0]

        entrada = {
            'data': data, 'qt_entrada': qt_entrada
        }

        return entrada
    else:
        print("O produto não tem entradas!")
        return None