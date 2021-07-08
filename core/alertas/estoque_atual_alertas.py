import dateutil.utils
from core.alertas.verificador import get_filiais
from api.models.estoque_atual import EstoqueAtual
import pandas as pd
import datetime


def estoque_atual(cod_produto, id_empresa):
    global disponivel
    hoje = datetime.date.today()

    filiais = get_filiais(id_empresa)

    list = []
    for filial in filiais:

        estoque_a = pd.DataFrame(EstoqueAtual.objects.filter(
            cod_produto__exact=cod_produto,
            cod_filial__exact=filial.cod_filial,
            data=hoje,
            empresa__id__exact=id_empresa
        ).order_by('-id').values())

        if not estoque_a.empty:
            estoque_ = estoque_a.drop_duplicates(subset=['cod_filial'], keep='first')
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
