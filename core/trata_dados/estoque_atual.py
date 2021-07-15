from api.models.estoque_atual import EstoqueAtual
import pandas as pd
import datetime


def estoque_atual(cod_produto, id_empresa):
    estoque_a = pd.DataFrame(EstoqueAtual.objects.filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa
    )[:1].values())

    if not estoque_a.empty:
        data = estoque_a['data'][0]
        qt_disponivel = estoque_a['qt_disponivel'][0]
        qt_inden = estoque_a['qt_indenizada'][0]
        pr_custo = estoque_a['custo_ult_ent'][0]
        pr_venda = estoque_a['preco_venda'][0]

        disp = {
            'data': [data], 'qt_disponivel': [qt_disponivel], 'qt_indenizada': qt_inden, 'preco_venda': pr_venda,
            'preco_custo': pr_custo
        }
        disponivel = pd.DataFrame(disp)

        print("ESTOQUE ATUAL - OK")
        print("##############################")

        return disponivel
    else:
        print("ESTOQUE ATUAL - O PRODUTO NÃO ESTOQUE")
        print("##############################")

        return None