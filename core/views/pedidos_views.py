from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models.pedidos_models import *
from django.shortcuts import get_list_or_404, get_object_or_404


@login_required
def pedido_painel(request, template_name='aplicacao/paginas/pedidos/pedidos.html'):
    id_empresa = request.user.usuario.empresa_id
    pedidos = PedidoInsight.objects.filter(empresa__id=id_empresa)

    contexto = {
        'pedidos': pedidos
    }

    return render(request, template_name, contexto)


@login_required
def ver_pedidos_insight(request, pk, template_name='aplicacao/paginas/pedidos/ver-pedido.html'):
    pedido = PedidoInsight.objects.get(id=pk)
    itens = PedidoInsightItens.objects.filter(pedido=pedido.pk)

    contexto = {
        'itens':itens,
        'pedido': pedido
    }

    return render(request, template_name, contexto)