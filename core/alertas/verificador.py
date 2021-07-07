import datetime
from api.models.venda import Venda


def verifica_produto(cod_produto, id_empresa, periodo):

    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    vendas =Venda.objects.filter(
        cod_produto__exact=cod_produto,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=id_empresa
    ).exists()

    if vendas:
        return True
    else:
        return False