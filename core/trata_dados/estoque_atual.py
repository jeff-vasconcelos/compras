from api.models.estoque_atual_models import EstoqueAtual
import pandas as pd
import datetime


def estoque_atual(cod_produto, id_empresa):
    # CONSULTANDO VENDAS NO BANCO DE DADOS
    estoque_a = pd.DataFrame(EstoqueAtual.objects.filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa,
        data=datetime.date.today()
    )[:1].values())

    if not estoque_a.empty:
        data = estoque_a['data'][0]
        qt_disponivel = estoque_a['qt_disponivel'][0]
        qt_inden = estoque_a['qt_indenizada'][0]

        disp = {
            'data': [data], 'qt_disponivel': [qt_disponivel], 'qt_indenizada': qt_inden
        }
        disponivel = pd.DataFrame(disp)

        return disponivel
    else:
        print("O produto não tem registro de estoque!")
        return None