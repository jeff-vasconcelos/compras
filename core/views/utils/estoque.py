import pandas as pd
from api.models.estoque import Estoque

from core.views.alerta.verificador import get_filiais


def estoque_atual(cod_produto, id_empresa, lista_filiais=''):
    global results_estoque

    lista_estoque = []
    if lista_filiais:
        for filial in lista_filiais:
            results_estoque = qs_estoque(cod_produto=cod_produto, filial=filial, id_empresa=id_empresa,
                                         lista_estoque=lista_estoque)

        return process_estoque(results_estoque)

    else:
        filiais = get_filiais(id_empresa)

        for f in filiais:
            results_estoque = qs_estoque(cod_produto=cod_produto, filial=f.cod_filial, id_empresa=id_empresa,
                                         lista_estoque=lista_estoque)
        return process_estoque(lista_estoque=results_estoque)


def qs_estoque(cod_produto, filial, id_empresa, lista_estoque):
    estoque_a = pd.DataFrame(Estoque.objects.filter(
        cod_produto__exact=cod_produto,
        cod_filial__exact=filial,
        empresa__id__exact=id_empresa
    ).order_by('-id')[:1].values())

    print(cod_produto)

    if not estoque_a.empty:
        estoque_ = estoque_a.drop_duplicates(subset=['cod_filial'], keep='first')
        lista = estoque_.values.tolist()
        lista_estoque.append(lista)

    return lista_estoque


def process_estoque(lista_estoque):
    global disponivel_est, lista_fim
    list_est_atual = []
    lista_fim = []

    for i in lista_estoque:
        df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial", "cod_fornecedor", "qt_geral", "qt_indenizada",
                                      "qt_reservada", "qt_pendente", "qt_bloqueada", "qt_disponivel", "preco_venda",
                                      "custo_ult_entrada", "data", "created_at", "produto_id", "fornecedor_id",
                                      "filial_id",
                                      "empresa_id", "campo_um", "campo_dois", "campo_tres"
                                      ])

        df.drop(columns=["campo_um", "campo_dois", "campo_tres"], inplace=True)

        disponivel = df
        disponiveis = disponivel.assign(
            **disponivel.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

        list_est_atual.append(disponiveis)

        for a in list_est_atual:
            for b in a:
                lista_fim.append(b)

    disponivel_est = pd.DataFrame(lista_fim)

    return disponivel_est
