import dateutil.utils
from core.models.empresas_models import Filial
from api.models.estoque_atual import EstoqueAtual
import pandas as pd
import datetime


def estoque_atual(cod_produto, id_empresa):
    hoje = datetime.date.today()
    estoque_a = pd.DataFrame(EstoqueAtual.objects.filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa,
        data=hoje
    ).order_by('-id').values())

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    if not estoque_a.empty:
        estoque_a = estoque_a.drop_duplicates(subset=['cod_filial'], keep='first')

        list = []
        for filial in filiais:
            estoque_ = estoque_a
            estoque_ = estoque_.query('cod_filial == @filial.cod_filial')
            lista = estoque_.values.tolist()
            list.append(lista)

        list_est_atual = []
        for i in list:
            df = pd.DataFrame(i, columns=["id", "cod_produto", "desc_produto", "embalagem", "cod_filial", "filial_id",
                                          "cod_fornecedor", "produto_id", "fornecedor_id", "empresa_id",
                                          "qt_estoque_geral", "qt_indenizada", "qt_reservada", "qt_pendente",
                                          "qt_bloqueada", "qt_disponivel", "custo_ult_ent", "preco_venda", "data",
                                          "created_at"])
            disponivel = df
            disponiveis = disponivel.assign(
                **disponivel.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

            list_est_atual.append(disponiveis)

            lista_fim = []
            for a in list_est_atual:
                for b in a:
                    lista_fim.append(b)

            disponivel = pd.DataFrame(lista_fim)

        return disponivel
    else:
        return None
