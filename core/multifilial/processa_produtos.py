from django.shortcuts import render
from core.multifilial.curva_abc import abc
from core.multifilial.estoque_atual import estoque_atual
from core.multifilial.historico_estoque import historico_estoque
from core.multifilial.pedidos import pedidos_compra


def processa_produtos_filiais(request, template_name='aplicacao/paginas/teste_remover.html'):
    empresa = request.user.usuario.empresa_id
    forn = [111]
    produto = 999

    #CURVA ABC
    curva = abc(forn, empresa, 90)
    lista_curva_abc = curva.to_dict('records')
    #print(lista_curva_abc)

    #ESTOQUE ATUAL
    est_atual_atual = estoque_atual(produto, empresa)
    lista_est_atual = est_atual_atual.to_dict('records')
    #print(e_atual)

    #HISTORICO DE ESTOQUE
    h_estoque = historico_estoque(produto, empresa, 90)
    lista_hist_estoq = h_estoque.to_dict('records')

    #PEDIDOS
    pedidos = pedidos_compra(produto, empresa)
    print(pedidos)




    contexto = {
        'curva': lista_curva_abc,
        'estoque': lista_est_atual,
        'historico': lista_hist_estoq
    }
    return render(request, template_name, contexto)
