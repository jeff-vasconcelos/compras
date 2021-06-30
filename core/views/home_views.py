from django.shortcuts import render
from core.multifilial.processa_produtos import processa_produtos_filiais

def home_painel(request, template_name='aplicacao/paginas/home.html'):
    processa_produtos_filiais(request)
    return render(request, template_name)
