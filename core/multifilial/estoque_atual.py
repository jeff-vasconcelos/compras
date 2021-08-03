import dateutil.utils
from core.models.empresas_models import Filial
from api.models.estoque_atual import Estoque
import pandas as pd
import datetime

from core.multifilial.filiais import get_filiais


def estoque_atual(cod_produto, id_empresa, lista_filiais):
    global disponivel
    # hoje = datetime.date.today()

    # filiais = get_filiais(id_empresa)

    list = []
    for filial in lista_filiais:

        estoque_a = pd.DataFrame(Estoque.objects.filter(
            cod_produto__exact=cod_produto,
            cod_filial__exact=filial,
            empresa__id__exact=id_empresa
        )[:1].values())

        if not estoque_a.empty:
            estoque_ = estoque_a.drop_duplicates(subset=['cod_filial'], keep='first')
            lista = estoque_.values.tolist()
            list.append(lista)

    list_est_atual = []
    for i in list:
        df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial",  "cod_fornecedor", "qt_geral", "qt_indenizada",
                                      "qt_reservada", "qt_pendente", "qt_bloqueada", "qt_disponivel", "preco_venda",
                                      "custo_ult_entrada", "data", "created_at", "produto_id", "fornecedor_id", "filial_id",
                                      "empresa_id", "campo_um", "campo_dois", "campo_tres"
                                      ])

        df.drop(columns=["campo_um", "campo_dois", "campo_tres"], inplace=True)

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
