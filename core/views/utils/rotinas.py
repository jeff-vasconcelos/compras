from django.shortcuts import render
from core.views.alerta.alertas_views import send_email_alerta, alerta_db
from core.views.home.functions_home import save_grafico_curva, save_grafico_faturamento, save_dados_estoque
from core.views.alerta.processa_produtos import *
from api.views import valida_pedidos_excluidos
from core.models.empresas_models import Empresa
from api.models.pedido_duplicado import PedidoDuplicado


# ROTINA DE EXECUÇÃO DE ALERTA
def rotina_alerta(request, id_empresa):
    empresa = Empresa.objects.get(id=id_empresa)
    print(f"PROCESSANDO DADOS DE {empresa.id} - {empresa.nome_fantasia}")

    # Executa e processa dados de alerta
    produtos_alerta = processa_produtos_alerta_home(id_empresa, curva_home=False)

    # Executa e processa dados de home
    produtos_home = processa_produtos_alerta_home(id_empresa, curva_home=True)

    save_grafico_curva(id_empresa, produtos_home)
    save_grafico_faturamento(id_empresa)
    save_dados_estoque(id_empresa, produtos_home)
    alerta_db(id_empresa, produtos_alerta)


# ROTINA DE EXECUÇÃO DE EMAIL
def rotina_email(request, id_empresa):
    empresa = Empresa.objects.get(id=id_empresa)
    pedidos_existentes = PedidoDuplicado.objects.filter(empresa__id=id_empresa)

    # TODO testando pedido excluido do winthor
    valida_pedidos_excluidos(id_empresa)
    pedidos_existentes.delete()

    # SE HABILITADA A OPÇÃO DE ENVIO DE EMAIL - CADASTRO DA EMPRESA
    try:
        if empresa.envia_email:
            print(f"ENVIANDO EMAIL(S) DE {empresa.nome_fantasia}")
            send_email_alerta(request, id_empresa)
    except:
        print("NÃO FOI POSSIVEL ENVIAR O(S) EMAIL(S)")


# TODO FUNÇÃO DE TESTE - REMOVER
def teste(request, template_name='testando_alerta.html'):
    id_empresa=1
    empresa = Empresa.objects.get(id=id_empresa)
    print(f"PROCESSANDO DADOS DE {empresa.id} - {empresa.nome_fantasia}")

    produtos_alerta = processa_produtos_alerta_home(id_empresa, curva_home=False)
    produtos_home = processa_produtos_alerta_home(id_empresa, curva_home=True)

    save_grafico_curva(id_empresa, produtos_home)
    save_grafico_faturamento(id_empresa)
    save_dados_estoque(id_empresa, produtos_home)
    alerta_db(id_empresa, produtos_alerta)

    return render(request, template_name)
