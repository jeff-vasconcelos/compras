from core.alertas.processa_produtos_alertas import *
from core.alertas.verificador import *
import numpy as np


def alertas():
    global alertas_produtos, infor_produtos_filiais, condicao
    id_empresa = 1
    lista_alertas = []
    parametros = Parametro.objects.get(empresa_id=id_empresa)

    fornecedores = get_fornecedores(id_empresa)

    for fornecedor in fornecedores:
        print(fornecedor)
        leadtime = fornecedor.leadtime
        t_reposicao = fornecedor.ciclo_reposicao
        produtos = get_produtos(id_empresa, fornecedor.id)

        for produto in produtos:
            print(produto.desc_produto)

            verif_produto = verifica_produto(produto.cod_produto, id_empresa, parametros.periodo)

            if verif_produto == True:
                infor_produtos_filiais = processa_produtos_filiais(
                    produto.cod_produto,
                    fornecedor.cod_fornecedor,
                    id_empresa,
                    leadtime,
                    t_reposicao,
                    parametros.periodo
                )

                infor_produtos_filiais['cod_produto'] = produto.cod_produto
                infor_produtos_filiais['desc_produto'] = produto.desc_produto
                infor_produtos_filiais['fornecedor'] = fornecedor.desc_fornecedor
                infor_produtos_filiais['cod_fornecedor'] = fornecedor.cod_fornecedor

                condicao = ['FALSE' if x == 'NORMAL' else 'TRUE' for x in infor_produtos_filiais['condicao_estoque']]

                if "FALSE" in condicao:
                    print("vai para o alerta")
                    alertas_produtos = infor_produtos_filiais.to_dict('records')
                    lista_alertas.append(alertas_produtos)

    return lista_alertas


def alerta_painel(request, template_name='aplicacao/paginas/alertas.html'):
    produtos = alertas()
    lista_alerta = []
    for i in produtos:
        produto = i
        for a in produto:
            lista_alerta.append(a)
    print(lista_alerta)

    return render(request, template_name, {'produtos': lista_alerta})
