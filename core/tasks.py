from __future__ import absolute_import
from celery import shared_task
from core.views.utils.rotinas import *


@shared_task
def processa_alerta(request, id_empresa):
    print("INICIANDO TASK DE ALERTAS...")
    rotina_alerta(request, id_empresa)
    print("TASK DE ALERTAS CONCLUIDA!")


@shared_task
def processa_email(request, id_empresa):
    print("INICIANDO TASK DE EMAIL...")
    rotina_email(request, id_empresa)
    print("TASK DE EMAIL CONCLUIDA!")


@shared_task
def processa_teste(id_empresa):
    print("INICIANDO TASK DE TESTES...")
    teste(id_empresa)
    print("TASK DE TESTES CONCLUIDA!")