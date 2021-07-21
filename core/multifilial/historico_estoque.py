from api.models.historico_estoque import HistoricoEstoque
from core.models.empresas_models import Filial
import pandas as pd
import datetime


def historico_estoque(cod_produto, id_empresa, periodo):
    global historico
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    # CONSULTANDO VENDAS NO BANCO DE DADOS
    h_estoque = pd.DataFrame(HistoricoEstoque.objects.filter(
        cod_produto__exact=cod_produto,
        data__range=[data_fim, data_inicio],
        empresa__id__exact=id_empresa
    ).values())

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    if not h_estoque.empty:

        list = []
        for filial in filiais:
            estoque_h = h_estoque
            estoque_h = estoque_h.query('cod_filial == @filial.cod_filial')
            lista = estoque_h.values.tolist()
            list.append(lista)

        list_est_histor = []
        for i in list:
            df = pd.DataFrame(i, columns=["id", "cod_produto", "desc_produto", "embalagem", "cod_filial", "filial_id",
                                          "cod_fornecedor", "produto_id", "fornecedor_id", "empresa_id",
                                          "qt_estoque", "data", "created_at"])
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
    else:
        return None