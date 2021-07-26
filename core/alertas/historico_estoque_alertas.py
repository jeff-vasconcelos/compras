from api.models.historico_estoque import HistoricoEstoque
from core.alertas.verificador import get_filiais
import pandas as pd
import datetime


def historico_estoque(cod_produto, id_empresa, periodo):
    global historico
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    filiais = get_filiais(id_empresa)

    list = []
    for filial in filiais:

        h_estoque = pd.DataFrame(HistoricoEstoque.objects.filter(
            cod_produto__exact=cod_produto,
            cod_filial__exact=filial.cod_filial,
            data__range=[data_fim, data_inicio],
            empresa__id__exact=id_empresa
        ).values())

        if not h_estoque.empty:
            estoque_h = h_estoque
            lista = estoque_h.values.tolist()
            list.append(lista)

    list_est_histor = []
    for i in list:
        df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial", "cod_fornecedor", "qt_estoque", "data",
                                      "created_at", "produto_id", "fornecedor_id", "filial_id", "empresa_id"])
        historico = df
        hist_estoque = historico.assign(
            **historico.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

        list_est_histor.append(hist_estoque)

        lista_fim = []
        for a in list_est_histor:
            for b in a:
                lista_fim.append(b)

        historico = pd.DataFrame(lista_fim)


    return historico
