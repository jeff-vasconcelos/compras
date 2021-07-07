from core.alertas.fornecedor_alertas import get_fornecedores
from core.alertas.produto_alertas import get_produtos
from core.alertas.processa_produtos_alertas import *
from core.alertas.vendas_alertas import *


def alertas():
    id_empresa = 1
    lista_alertas = []

    fornecedores = get_fornecedores(id_empresa)

    for fornecedor in fornecedores:
        print(fornecedor)
        leadtime = fornecedor.leadtime
        t_reposicao = fornecedor.ciclo_reposicao
        produtos = get_produtos(id_empresa, fornecedor.id)
        for produto in produtos:
            print(produto.desc_produto)
            infor_produtos_filiais = processa_produtos_filiais(produto.id, id_empresa, leadtime, t_reposicao)

            if infor_produtos_filiais is not None:
                alertas_produtos = infor_produtos_filiais.to_dict('records')
    lista_alertas.append(alertas_produtos)
    print(lista_alertas)

def alerta_painel(request, template_name='aplicacao/paginas/alertas.html'):
    vendas(10, 1, 30)
    return render(request, template_name)