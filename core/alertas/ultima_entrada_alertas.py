from api.models.ultima_entrada import Entrada
from core.alertas.verificador import get_filiais
import pandas as pd
import datetime


def ultima_entrada(cod_produto, id_empresa, periodo):
    global entrada
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    filiais = get_filiais(id_empresa)

    list = []
    list_entradas = []
    for filial in filiais:

        u_entrada_df = pd.DataFrame(Entrada.objects.filter(
            cod_produto__exact=cod_produto,
            cod_filial__exact=filial.cod_filial,
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
            df = pd.DataFrame(i, columns=["id", "cod_produto", "desc_produto", "cod_filial", "filial_id",
                                          "cod_fornecedor", "produto_id", "fornecedor_id", "empresa_id",
                                          "qt_ult_entrada", "vl_ult_entrada", "data", "created_at"])
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