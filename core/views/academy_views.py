from django.shortcuts import render
from core.models.academy_models import *

def teste(request, template_name='aplicacao/paginas/academy/academy.html'):
    return render(request, template_name)

def paginacao(request, slug):
    videos = Academy.objects.get(slug=slug)

    nextpost = Academy.objects.filter(id__gt=videos.id).order_by('id').first()
    prevpost = Academy.objects.filter(id__lt=videos.id).order_by('id').last()

    return render(request, 'aplicacao/paginas/academy/academy_video.html',
                  {'video': videos, 'prevpost': prevpost,'nextpost': nextpost})

def PaginaPublico(request, slug):
    pagina = get_object_or_404(Pagina, slug=slug)

    context = {'page':pagina, 'arquivos':arquivos}

    return render(request, "publico/paginas/pagina.html", context)