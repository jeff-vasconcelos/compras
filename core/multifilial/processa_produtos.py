from django.shortcuts import render
from core.multifilial.curva_abc import abc
from core.multifilial.estoque_atual import estoque_atual


def processa_produtos_filiais(request, template_name='aplicacao/paginas/teste_remover.html'):
    empresa = request.user.usuario.empresa_id
    forn = [111]
    produto = 999
    curva = abc(forn, empresa, 90)
    #print(curva)
    lista_curva_abc = curva.to_dict('records')
    #print(lista_curva_abc)

    e_atual = estoque_atual(produto, empresa)
    #print(e_atual)

    return render(request, template_name, {'curva': lista_curva_abc})
