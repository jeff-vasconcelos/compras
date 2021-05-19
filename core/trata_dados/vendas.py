from api.models.vendas_models import Venda
import pandas as pd
from scipy.stats import norm
import datetime


def vendas(id_produto, id_empresa):
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=119)

    vendas = Venda.objects.filter(
        produto__produto_id=id_produto,
        empresa
        data__range=[data_inicio, data_fim]
    )