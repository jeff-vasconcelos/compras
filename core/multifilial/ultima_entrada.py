from api.models.ultima_entrada import Entrada
from core.models.empresas_models import Filial
import pandas as pd
import datetime


def ultima_entrada(cod_produto, id_empresa, periodo):
    data_inicio = datetime.date.today()
    data_fim = data_inicio - datetime.timedelta(days=periodo - 1)  # Aqui sempre será o periodo informado -1

    u_entrada_df = pd.DataFrame(Entrada.objects.filter(
        cod_produto__exact=cod_produto,
        empresa__id__exact=id_empresa,
        data__range=[data_fim, data_inicio]
    ).order_by('-id').values())

    filiais = Filial.objects.filter(empresa__id__exact=id_empresa)

    if not u_entrada_df.empty:
        u_entrada_df = u_entrada_df.drop_duplicates(subset=['cod_filial'], keep='first')

        list = []
        for filial in filiais:
            u_entrada_ = u_entrada_df
            u_entrada_ = u_entrada_.query('cod_filial == @filial.cod_filial')
            lista = u_entrada_.values.tolist()
            list.append(lista)

        list_entradas = []
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