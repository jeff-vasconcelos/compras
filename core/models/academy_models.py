from django.db import models
from django.utils.text import slugify


class Academy(models.Model):
    titulo = models.CharField(max_length=255, blank=True, null=True)
    cod_video = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)

    class Meta:
        verbose_name = 'Academy'
        verbose_name_plural = 'Academy'

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.titulo)}'
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo