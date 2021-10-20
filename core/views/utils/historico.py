import pandas as pd
from api.models.historico import Historico
from core.views.alerta.verificador import get_filiais
from core.views.utils.datas import intervalo_periodo


def historico_estoque(cod_produto, id_empresa, periodo, lista_filiais=''):
    lista_historico = []
    global results_lista
    if lista_filiais:
        for filial in lista_filiais:
            results_lista = qs_historico(cod_produto=cod_produto, filial=filial,
                                         periodo=periodo, id_empresa=id_empresa, lista_historico=lista_historico)

        return process_historico(results_lista)

    else:
        filiais = get_filiais(id_empresa)
        for filial in filiais:
            # print('executou')
            results_lista = qs_historico(cod_produto=cod_produto, filial=filial.cod_filial,
                                         periodo=periodo, id_empresa=id_empresa, lista_historico=lista_historico)

        return process_historico(results_lista)

def qs_historico(cod_produto, filial, periodo, id_empresa, lista_historico):
    inicio, fim = intervalo_periodo(periodo)

    h_estoque = pd.DataFrame(Historico.objects.filter(
        cod_produto__exact=cod_produto,
        cod_filial__exact=filial,
        data__range=[fim, inicio],
        empresa__id__exact=id_empresa
    ).values())

    if not h_estoque.empty:
        estoque_h = h_estoque
        lista = estoque_h.values.tolist()
        lista_historico.append(lista)
    return lista_historico


def process_historico(lista_historico):

    global historico, lista_fim
    list_est_histor=[]
    for i in lista_historico:
        df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial", "cod_fornecedor", "qt_estoque", "data",
                                      "created_at", "produto_id", "fornecedor_id", "filial_id", "empresa_id",
                                      "campo_um", "campo_dois", "campo_tres"
                                      ])

        df.drop(columns=["campo_um", "campo_dois", "campo_tres"], inplace=True)

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
