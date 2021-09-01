from api.models.ultima_entrada import Entrada
from core.models.empresas_models import Filial
import pandas as pd
import datetime

from core.multifilial.filiais import get_filiais


def ultima_entrada(cod_produto, id_empresa, periodo, lista_filiais):
    global entrada
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    # filiais = get_filiais(id_empresa)

    list = []
    list_entradas = []
    for filial in lista_filiais:

        u_entrada_df = pd.DataFrame(Entrada.objects.filter(
            cod_produto__exact=cod_produto,
            cod_filial__exact=filial,
            data__range=[data_fim, data_inicio],
            empresa__id__exact=id_empresa
        ).order_by('-id').values())

        if not u_entrada_df.empty:
            u_entrada_df = u_entrada_df.drop_duplicates(subset=['cod_filial'], keep='first')
            u_entrada_ = u_entrada_df
            lista = u_entrada_.values.tolist()
            list.append(lista)

    if list:
        for i in list:
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