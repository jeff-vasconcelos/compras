from django.shortcuts import render
from core.models.academy_models import *
from django.contrib.auth.decorators import login_required


@login_required
def academy(request, template_name='aplicacao/paginas/academy/academy.html'):
    videos = Academy.objects.all()
    return render(request, template_name, {'videos': videos})


@login_required
def video_academy(request, slug, template_name='aplicacao/paginas/academy/academy_video.html'):
    video = Academy.objects.get(slug=slug)
    nextacad = Academy.objects.filter(id__gt=video.id).order_by('id').first()
    prevacad = Academy.objects.filter(id__lt=video.id).order_by('id').last()

    return render(request, template_name,
                  {'video': video, 'prevacad': prevacad, 'nextacad': nextacad})
