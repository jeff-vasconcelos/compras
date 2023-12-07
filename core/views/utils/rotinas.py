import datetime

from django.utils import timezone
from django.shortcuts import render

from app.models.pedido import Pedido
from core.views.alerta.alertas_views import send_email_alerta, alerta_db
from core.views.home.functions_home import save_grafico_curva, save_grafico_faturamento, save_dados_estoque
from core.views.alerta.processa_produtos import *
from core.models.empresas_models import Empresa
# from app.models.pedido_duplicado import PedidoDuplicado
from django.db.models import Q
from datetime import date, timedelta


# ROTINA DE EXECUÇÃO DE ALERTA
def rotina_alerta(id_empresa):
    empresa = Empresa.objects.get(id=id_empresa)
    print(f"PROCESSANDO DADOS (ALERTA) DE {empresa.id} - {empresa.nome_fantasia}")
    parametros = Parametro.objects.get(empresa__id=id_empresa)
    curva_filial = []

    # Executa e processa dados de alerta
    produtos_alerta = processa_produtos_alerta_home(id_empresa, parametros.periodo, curva_filial, curva_home=False)

    alerta_db(id_empresa, produtos_alerta)


# ROTINA DE EXECUÇÃO DE HOME
def rotina_home(id_empresa):
    empresa = Empresa.objects.get(id=id_empresa)
    print(f"PROCESSANDO DADOS (HOME) DE {empresa.id} - {empresa.nome_fantasia}")

    # Executa e processa dados de home
    parametros = Parametro.objects.get(empresa__id=id_empresa)
    curva_filial = abc_home(id_empresa, parametros.periodo)
    produtos_home = processa_produtos_alerta_home(id_empresa, parametros.periodo, curva_filial, curva_home=True)

    print("SALVANDO DADOS EM GRAFICOS")
    save_grafico_curva(id_empresa, produtos_home)
    save_grafico_faturamento(id_empresa)
    save_dados_estoque(id_empresa, produtos_home)

    data_hora = datetime.datetime.now(tz=timezone.utc)
    empresa.atualizacao_home = data_hora
    empresa.save()

    # valida_pedidos_excluidos(id_empresa)


# ROTINA DE EXECUÇÃO DE EMAIL
def rotina_email(request, id_empresa):
    empresa = Empresa.objects.get(id=id_empresa)

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
    curva_filial = ''

    produtos_alerta = processa_produtos_alerta_home(id_empresa, 120, curva_filial, curva_home=False)

    curva_filial = abc_home(id_empresa, 120)

    # Executa e processa dados de home
    produtos_home = processa_produtos_alerta_home(id_empresa, 120, curva_filial, curva_home=True)


    save_grafico_curva(id_empresa, produtos_home)
    save_grafico_faturamento(id_empresa)
    save_dados_estoque(id_empresa, produtos_home)
    alerta_db(id_empresa, produtos_alerta)

    # valida_pedidos_excluidos(id_empresa)

    return render(request, template_name)


# def valida_pedidos_excluidos(id_empresa):
#     global pedidos
#     pedidos_existentes = PedidoDuplicado.objects.filter(empresa__id=id_empresa)
#     lista_produtos_ped = []
#
#     if pedidos_existentes:
#         for i in pedidos_existentes:
#             lista_produtos_ped.append(i.cod_produto)
#
#         existe = list(set(lista_produtos_ped))
#
#         #hoje = date.today()
#
#         pedidos = Pedido.objects.filter(
#             empresa__id=id_empresa
#         ).exclude(Q(cod_produto__in=existe))
#         #).exclude(Q(cod_produto__in=existe) | Q(created_at=hoje))
#
#         if pedidos:
#
#             pedidos.delete()
#             pedidos_existentes.delete()
#
#     return None
