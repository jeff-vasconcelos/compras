from __future__ import absolute_import
from celery import shared_task
from core.views.alertas_views import rotina_alerta_home


@shared_task
def realiza_alerta(request):
    print("Realizando rotina de alerta HOME...")
    rotina_alerta_home(request)
    print("Rotina de alerta concluido!!!")
