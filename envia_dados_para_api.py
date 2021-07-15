import pandas as pd
import requests
import datetime
import json


def login_api():
    usuario = 'cluster'
    senha = 'Cluster*2018'

    url = "http://127.0.0.1:8000/api-token-auth"
    user_data = {
        "username": usuario,
        "password": senha
    }

    response = requests.post(url=url, json=user_data)

    if response.status_code == 200:
        response_data = response.json()
        token_puro = response_data['token']

        token = "Token "
        token += token_puro
        return token


def produtos():
    df_produtos = pd.read_csv(
        'https://raw.githubusercontent.com/cluster-desenvolvimento/news-datasets/main/SKUs.csv',
        sep=';')

    df_produtos.columns = ["cod_produto", "desc_produto", "embalagem", "quantidade_un_cx", "marca", "peso_liq",
                           "cod_fornecedor"]
    df_produtos['filial'] = 1

    df_produtos['quantidade_un_cx'] = df_produtos['quantidade_un_cx'].replace(",", ".", regex=True).astype(float).round(3)

    produtos_dic = df_produtos.assign(**df_produtos.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict(
        "records")

    print(df_produtos)
    print(df_produtos.info())
    dados = produtos_dic
    token = login_api()

    url = "http://127.0.0.1:8000/api/produto/"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'dataType': 'json',
        'Accept': 'application/json'
    }

    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        for i in dados:
            data = json.dumps(i)
            response = requests.post(url=url, headers=headers, data=data)
            print(data)
        return response.status_code
    else:
        token = login_api()


def vendas():
    df_historico_vendas = pd.read_csv(
        'https://raw.githubusercontent.com/cluster-desenvolvimento/news-datasets/main/Insight_Vendas.csv', sep=';')

    df_historico_vendas.columns = ["cod_filial", "data", "cod_produto", "desc_produto", "qt_vendas", "preco_unit",
                                   "cliente", "peso_liquido", "cod_depto", "desc_dois", "num_nota", "cod_usur",
                                   "cod_fornecedor", "qt_unit_caixa", "cod_aux", "custo_fin", "marca",
                                   "cod_fab", "supervisor"]

    vendas_df = df_historico_vendas
    vendas_df = vendas_df.drop(columns=['cod_aux'])
    vendas_df['preco_unit'] = vendas_df['preco_unit'].replace(",", ".", regex=True).astype(float).round(3)
    vendas_df['peso_liquido'] = vendas_df['peso_liquido'].replace(",", ".", regex=True).astype(float)
    vendas_df['custo_fin'] = vendas_df['custo_fin'].replace(",", ".", regex=True).astype(float).round(3)
    vendas_df['data'] = pd.to_datetime(vendas_df['data'])
    vendas_df['empresa'] = 1

    vendas_df = vendas_df.query('cod_produto == 183')

    vendas_dic = vendas_df.assign(**vendas_df.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

    dados = vendas_dic
    token = login_api()

    url = "http://127.0.0.1:8000/api/venda/"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'dataType': 'json',
        'Accept': 'application/json'
    }

    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        for i in dados:
            data = json.dumps(i)
            response = requests.post(url=url, headers=headers, data=data)
            print(data)
        return response.status_code
    else:
        token = login_api()


def pedidos():
    df_pedidos_compras = pd.read_csv(
        'https://raw.githubusercontent.com/cluster-desenvolvimento/news-datasets/main/Insight_PedidoCompras.csv', sep=';')

    df_pedidos_compras.columns = ["cod_filial", "cod_produto", "desc_produto", "saldo", "num_pedido", "data"]
    df_pedidos_compras['data'] = pd.to_datetime(df_pedidos_compras['data'])
    df_pedidos_compras.fillna(0, inplace=True)

    pedidos_df = df_pedidos_compras
    pedidos_df['empresa'] = 1
    pedidos_df['cod_fornecedor'] = 16

    p_compras = pedidos_df.assign(**pedidos_df.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict("records")

    dados = p_compras
    token = login_api()

    url = "http://127.0.0.1:8000/api/pedido-compra/"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'dataType': 'json',
        'Accept': 'application/json'
    }

    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        for i in dados:
            data = json.dumps(i)
            response = requests.post(url=url, headers=headers, data=data)
        return response.status_code
    else:
        token = login_api()


def entradas():
    df_entradas_prod = pd.read_csv(
        'https://raw.githubusercontent.com/cluster-desenvolvimento/news-datasets/main/Insight_Entrada.csv',
        sep=';')

    df_entradas_prod.columns = ["cod_filial", "cod_produto", "desc_produto", "data", "vl_ult_entrada", "qt_ult_entrada"]
    df_entradas_prod['vl_ult_entrada'] = df_entradas_prod['vl_ult_entrada'].replace(",", ".", regex=True).astype(float).round(3)
    df_entradas_prod['data'] = pd.to_datetime(df_entradas_prod['data'])
    df_entradas_prod.fillna(0, inplace=True)

    entradas_df = df_entradas_prod
    entradas_df['empresa'] = 1
    entradas_df['cod_fornecedor'] = 16

    entradas = entradas_df.assign(**entradas_df.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict(
        "records")

    dados = entradas
    token = login_api()

    url = "http://127.0.0.1:8000/api/ultima-entrada/"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'dataType': 'json',
        'Accept': 'application/json'
    }

    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        for i in dados:
            data = json.dumps(i)
            response = requests.post(url=url, headers=headers, data=data)
        return response.status_code
    else:
        token = login_api()


def historico_estoque():
    df_hist_estoque = pd.read_csv(
        'https://raw.githubusercontent.com/cluster-desenvolvimento/news-datasets/main/Insight_HistoricoEstoque.csv',
        sep=';')
    df_hist_estoque.columns = ["cod_filial", "cod_produto", "desc_produto", "embalagem", "data", "qt_estoque"]
    df_hist_estoque['data'] = pd.to_datetime(df_hist_estoque['data'])
    df_hist_estoque.fillna(0, inplace=True)

    historico_df = df_hist_estoque
    historico_df['empresa'] = 1
    historico_df['cod_fornecedor'] = 16

    historico = historico_df.assign(**historico_df.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict(
        "records")

    dados = historico
    token = login_api()

    url = "http://127.0.0.1:8000/api/historico-estoque/"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'dataType': 'json',
        'Accept': 'application/json'
    }

    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        for i in dados:
            data = json.dumps(i)
            response = requests.post(url=url, headers=headers, data=data)
        return response.status_code
    else:
        token = login_api()


def estoque():
    df_estoque_prod = pd.read_csv(
        'https://raw.githubusercontent.com/cluster-desenvolvimento/news-datasets/main/Insight_Estoque.csv',
        sep=';')
    df_estoque_prod.columns = ["cod_filial", "cod_produto", "desc_produto", "cod_fornecedor", "fornecedor", "embalagem",
                               "qt_estoque_geral", "qt_indenizada", "qt_reservada", "qt_pendente", "custo_ult_ent",
                               "preco_venda", "qt_bloqueada", "qt_disponivel"]
    df_estoque_prod['qt_disponivel'].fillna(0, inplace=True)
    df_estoque_prod['qt_estoque_geral'].fillna(0, inplace=True)
    df_estoque_prod['preco_venda'].fillna(0, inplace=True)

    df_estoque_prod['qt_disponivel'] = df_estoque_prod['qt_disponivel'].astype(int)
    df_estoque_prod['qt_estoque_geral'] = df_estoque_prod['qt_estoque_geral'].astype(int)
    df_estoque_prod['custo_ult_ent'] = df_estoque_prod['custo_ult_ent'].replace(",", ".", regex=True).astype(float).round(3)
    df_estoque_prod['preco_venda'] = df_estoque_prod['preco_venda'].replace(",", ".", regex=True).astype(float).round(3)
    df_estoque_prod = df_estoque_prod.drop(columns=['fornecedor'])
    df_estoque_prod['data'] = datetime.date.today()
    df_estoque_prod['data'] = pd.to_datetime(df_estoque_prod['data'])


    estoque_atual_df = df_estoque_prod

    estoque_atual_df['empresa'] = 1

    estoque_atual_df = estoque_atual_df.query('cod_produto == 183')

    estoque_atual = estoque_atual_df.assign(**estoque_atual_df.select_dtypes(["datetime"]).astype(str).to_dict("list")).to_dict(
        "records")

    dados = estoque_atual
    token = login_api()

    url = "http://127.0.0.1:8000/api/estoque-atual/"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'dataType': 'json',
        'Accept': 'application/json'
    }

    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        for i in dados:
            data = json.dumps(i)
            print(data)
            response = requests.post(url=url, headers=headers, data=data)
        return response.status_code
    else:
        token = login_api()


if __name__ == '__main__':
    produtos()
