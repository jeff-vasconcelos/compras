from __future__ import absolute_import
from celery import shared_task
from core.views.alertas_views import *


@shared_task
def processa_alerta(request, id_empresa):
    print("Iniciando Alertas...")
    rotina_alerta(request, id_empresa)
    print("Alerta concluido!")


@shared_task
def processa_email(request, id_empresa):
    print("Iniciando Envio de Emails...")
    rotina_email(request, id_empresa)
    print("Envio concluido!")