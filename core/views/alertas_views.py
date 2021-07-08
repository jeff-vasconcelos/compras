from core.alertas.processa_produtos_alertas import *
from core.alertas.vendas_alertas import *
from core.alertas.curva_abc_alertas import *
from core.alertas.estoque_atual_alertas import *
from core.alertas.historico_estoque_alertas import *
from core.alertas.pedidos_alertas import *

from core.alertas.verificador import *


def alertas():
    global alertas_produtos, infor_produtos_filiais
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

                alertas_produtos = infor_produtos_filiais.to_dict('records')
                lista_alertas.append(alertas_produtos)
            else:
                print('não tem vendas')
    print(lista_alertas)

def alerta_painel(request, template_name='aplicacao/paginas/alertas.html'):
    # vendas(10, 1, 30)
    alertas()
    # abc([11], 1, 30)
    # estoque_atual(13, 1)
    # historico_estoque(13, 1, 30)
    # pedidos_compra(10, 1)
    # ultima_entrada(13, 1, 30)

    # vendas_historico(13, 1, 30)
    # dados_produto(10, 11, 1, 15, 10, 30)
    # processa_produtos_filiais(10, 11, 1, 15, 30, 30)

    return render(request, template_name)