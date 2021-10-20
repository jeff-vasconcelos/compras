import pandas as pd
from api.models.entrada import Entrada
from core.views.alerta.verificador import get_filiais
from core.views.utils.datas import intervalo_periodo


def ultima_entrada(cod_produto, id_empresa, periodo, lista_filiais=''):
    global results_lista
    lista_entrada = []

    if lista_filiais:
        for filial in lista_filiais:
            results_lista = qs_ultima_entrada(cod_produto=cod_produto, filial=filial, periodo=periodo,
                                              id_empresa=id_empresa, lista_entrada=lista_entrada)

        return process_ultima_entrada(lista_entrada=results_lista)

    else:
        filiais = get_filiais(id_empresa)

        for filial in filiais:
            results_lista = qs_ultima_entrada(cod_produto=cod_produto, filial=filial.cod_filial, periodo=periodo,
                                              id_empresa=id_empresa, lista_entrada=lista_entrada)

        return process_ultima_entrada(lista_entrada=results_lista)


def qs_ultima_entrada(cod_produto, filial, periodo, id_empresa, lista_entrada):
    inicio, fim = intervalo_periodo(periodo)


    u_entrada_df = pd.DataFrame(Entrada.objects.filter(
        cod_produto__exact=cod_produto,
        cod_filial__exact=filial,
        empresa__id__exact=id_empresa,
        data__range=[fim, inicio]
    ).order_by('-id').values())

    if not u_entrada_df.empty:
        u_entrada_df = u_entrada_df.drop_duplicates(subset=['cod_filial'], keep='first')
        u_entrada_ = u_entrada_df
        lista = u_entrada_.values.tolist()
        lista_entrada.append(lista)

    return lista_entrada


def process_ultima_entrada(lista_entrada):
    global entrada
    list_entradas = []
    if lista_entrada:
        for i in lista_entrada:
            df = pd.DataFrame(i, columns=["id", "cod_produto", "cod_filial", "cod_fornecedor", "qt_ult_entrada",
                                          "vl_ult_entrada", "data", "created_at", "produto_id", "fornecedor_id",
                                          "filial_id", "empresa_id", "campo_um", "campo_dois", "campo_tres"
                                          ])

            df.drop(columns=["campo_um", "campo_dois", "campo_tres"], inplace=True)

            entrada = df
            entradas = entrada.assign(
                **entrada.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

            list_entradas.append(entradas)

            lista_fim = []
            for a in list_entradas:
                for b in a:
                    lista_fim.append(b)

            entrada = pd.DataFrame(lista_fim)

        return entrada

    else:
        return None